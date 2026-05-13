import os
import sqlite3
from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime
import re
from sqlalchemy import inspect

from models import db
from models.analysis import Analysis
from models.history import History
from models.settings import Setting
from services.text_processor import TextProcessor
from services.scoring_engine import ScoringEngine
from services.visualization_service import VisualizationService
from services.report_generator import ReportGenerator
from services.azure_text_analysis import AzureTextAnalysisService
from services.openai_service import OpenAIService
from modules.validators import Validators
from modules.database_manager import DatabaseManager
from modules.utilities import Utilities

load_dotenv()

app = Flask(__name__)
# Ensure database directory exists
db_dir = os.path.join(os.path.dirname(__file__), 'database')
os.makedirs(db_dir, exist_ok=True)

db_path = os.path.join(db_dir, 'ghostwriter.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if os.path.exists(db_path):
    try:
        with sqlite3.connect(db_path) as connection:
            connection.execute('PRAGMA quick_check')
    except sqlite3.DatabaseError:
        os.remove(db_path)

db.init_app(app)

with app.app_context():
    inspector = inspect(db.engine)
    existing_tables = set(inspector.get_table_names())
    for table_name, table in db.metadata.tables.items():
        if table_name not in existing_tables:
            table.create(bind=db.engine)

text_processor = TextProcessor()
scoring_engine = ScoringEngine()
visualization = VisualizationService()
report_generator = ReportGenerator()
azure_service = AzureTextAnalysisService()
openai_service = OpenAIService()

SETTING_ENV_MAP = {
    'azure_openai_api_key': 'AZURE_OPENAI_API_KEY',
    'azure_openai_endpoint': 'AZURE_OPENAI_ENDPOINT',
    'azure_openai_deployment_name': 'AZURE_OPENAI_DEPLOYMENT_NAME',
    'azure_text_analytics_api_key': 'AZURE_TEXT_ANALYTICS_API_KEY',
    'azure_text_analytics_endpoint': 'AZURE_TEXT_ANALYTICS_ENDPOINT'
}


def get_setting_value(setting_key):
    setting = Setting.query.filter_by(setting_key=setting_key).first()
    if setting and setting.setting_value.strip():
        return setting.setting_value.strip()
    return os.getenv(SETTING_ENV_MAP[setting_key], '').strip()


def get_effective_settings():
    return {key: get_setting_value(key) for key in SETTING_ENV_MAP}


def validate_credential_settings(settings_data):
    errors = {}

    for key in SETTING_ENV_MAP:
        if not settings_data.get(key, '').strip():
            errors[key] = 'This field is required.'

    for endpoint_key in ['azure_openai_endpoint', 'azure_text_analytics_endpoint']:
        endpoint = settings_data.get(endpoint_key, '').strip()
        if endpoint and (not endpoint.startswith('https://') or ' ' in endpoint):
            errors[endpoint_key] = 'Enter a valid HTTPS endpoint URL.'

    deployment_name = settings_data.get('azure_openai_deployment_name', '').strip()
    if deployment_name and not re.match(r'^[A-Za-z0-9._-]+$', deployment_name):
        errors['azure_openai_deployment_name'] = 'Use only letters, numbers, dots, dashes, or underscores.'

    for key in ['azure_openai_api_key', 'azure_text_analytics_api_key']:
        api_key = settings_data.get(key, '').strip()
        if api_key and len(api_key) < 10:
            errors[key] = 'API key looks too short.'

    return errors


def upsert_settings(settings_data):
    for key, value in settings_data.items():
        setting = Setting.query.filter_by(setting_key=key).first()
        if setting:
            setting.setting_value = value
        else:
            db.session.add(Setting(setting_key=key, setting_value=value))
    db.session.commit()


def configure_services_from_settings():
    settings_data = get_effective_settings()
    azure_service.initialize(
        endpoint=settings_data['azure_text_analytics_endpoint'],
        key=settings_data['azure_text_analytics_api_key']
    )
    openai_service.initialize(
        api_key=settings_data['azure_openai_api_key'],
        endpoint=settings_data['azure_openai_endpoint'],
        deployment_name=settings_data['azure_openai_deployment_name']
    )


@app.route('/')
def index():
    """Landing page"""
    stats = DatabaseManager.get_statistics()
    return render_template('index.html', stats=stats)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    current_settings = get_effective_settings()
    errors = {}
    success_message = None

    if request.method == 'POST':
        submitted_settings = {
            'azure_openai_api_key': request.form.get('azure_openai_api_key', '').strip(),
            'azure_openai_endpoint': request.form.get('azure_openai_endpoint', '').strip(),
            'azure_openai_deployment_name': request.form.get('azure_openai_deployment_name', '').strip(),
            'azure_text_analytics_api_key': request.form.get('azure_text_analytics_api_key', '').strip(),
            'azure_text_analytics_endpoint': request.form.get('azure_text_analytics_endpoint', '').strip()
        }

        updated_settings = current_settings.copy()
        for key, value in submitted_settings.items():
            if value:
                updated_settings[key] = value

        errors = validate_credential_settings(updated_settings)

        if not errors:
            upsert_settings({key: value for key, value in submitted_settings.items() if value})
            configure_services_from_settings()
            current_settings = get_effective_settings()
            success_message = 'Settings saved successfully.'

    return render_template(
        'settings.html',
        settings=current_settings,
        errors=errors,
        success_message=success_message
    )


@app.route('/dashboard')
def dashboard():
    """Dashboard with statistics"""
    stats = DatabaseManager.get_statistics()
    analyses = DatabaseManager.get_all_analyses()[:10]
    
    return render_template('dashboard.html',
                          total_analyses=stats['total'],
                          avg_human_score=stats['avg_human_score'],
                          avg_ai_score=stats['avg_ai_score'],
                          avg_readability=stats['avg_readability'],
                          recent_analyses=analyses)


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """Text analysis page"""
    configure_services_from_settings()

    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        
        # Validation
        valid, error = Validators.validate_text(text)
        if not valid:
            return render_template('analyze.html', error=error)
        
        # Process text
        metrics = text_processor.analyze_text(text)
        
        # Get sentiment from Azure
        sentiment_result = azure_service.analyze_sentiment(text)
        metrics['sentiment_label'] = sentiment_result.get('sentiment', 'neutral')
        
        # Calculate scores
        result = scoring_engine.calculate_scores(metrics)
        
        # Save to database
        analysis = DatabaseManager.save_analysis(
            text, metrics,
            result['human_score'],
            result['ai_score']
        )
        
        # Generate visualizations
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        chart1 = visualization.create_authenticity_gauge(
            result['human_score'],
            result['ai_score'],
            analysis.id
        )
        
        chart2 = visualization.create_metrics_radar(metrics, analysis.id)
        
        if len(sentences) > 1:
            chart3 = visualization.create_sentence_analysis(sentences, analysis.id)
        else:
            chart3 = None
        
        # Generate report
        report_text = report_generator.generate_text_report({
            'human_score': result['human_score'],
            'ai_score': result['ai_score'],
            'confidence': result['confidence'],
            **metrics
        })
        
        # Save history
        DatabaseManager.save_history(
            analysis.id,
            Utilities.truncate_text(text, 200),
            report_text
        )
        
        analysis_data = analysis.to_dict()
        analysis_data.update({
            'confidence': result['confidence'],
            'score_breakdown': result['score_breakdown'],
            'chart_authenticity': chart1,
            'chart_metrics': chart2,
            'chart_sentences': chart3,
            'report': report_text,
            'key_phrases': azure_service.extract_key_phrases(text)[:5]
        })
        
        return render_template('analyze.html', result=analysis_data)
    
    return render_template('analyze.html')


@app.route('/history')
def history():
    """Analysis history page"""
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'recent')
    
    analyses = DatabaseManager.get_all_analyses()
    
    if sort == 'high':
        analyses.sort(key=lambda x: x.human_score, reverse=True)
    elif sort == 'low':
        analyses.sort(key=lambda x: x.ai_score, reverse=True)
    
    # Pagination
    per_page = 10
    total = len(analyses)
    analyses = analyses[(page-1)*per_page : page*per_page]
    
    return render_template('history.html',
                          analyses=[a.to_dict() for a in analyses],
                          page=page,
                          total_pages=(total + per_page - 1) // per_page)


@app.route('/report/<int:analysis_id>')
def report(analysis_id):
    """Generate report for analysis"""
    analysis = DatabaseManager.get_analysis(analysis_id)
    
    if not analysis:
        return render_template('error.html', message='Analysis not found'), 404
    
    data = analysis.to_dict()
    history = History.query.filter_by(analysis_id=analysis_id).first()
    
    if history:
        data['report'] = history.generated_report
    
    return render_template('report.html', analysis=data)


@app.route('/api/analysis/<int:analysis_id>')
def api_analysis(analysis_id):
    """API endpoint for analysis data"""
    analysis = DatabaseManager.get_analysis(analysis_id)
    
    if not analysis:
        return jsonify({'error': 'Analysis not found'}), 404
    
    return jsonify(analysis.to_dict())


@app.route('/api/export/<int:analysis_id>')
def api_export(analysis_id):
    """Export analysis as JSON"""
    analysis = DatabaseManager.get_analysis(analysis_id)
    
    if not analysis:
        return jsonify({'error': 'Analysis not found'}), 404
    
    filepath = report_generator.save_json_report(analysis.to_dict(), analysis_id)
    return send_file(filepath, as_attachment=True)


@app.route('/api/export-text/<int:analysis_id>')
def api_export_text(analysis_id):
    """Export analysis as text"""
    analysis = DatabaseManager.get_analysis(analysis_id)
    
    if not analysis:
        return jsonify({'error': 'Analysis not found'}), 404
    
    data = analysis.to_dict()
    filepath = report_generator.save_text_report(data, analysis_id)
    return send_file(filepath, as_attachment=True)


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', message='Page not found'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', message='Server error'), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=os.getenv('FLASK_ENV') == 'development', port=port)
