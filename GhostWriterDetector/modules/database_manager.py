from models import db
from models.analysis import Analysis
from models.history import History
from datetime import datetime

class DatabaseManager:
    
    @staticmethod
    def save_analysis(original_text, metrics, human_score, ai_score):
        """Save analysis result to database"""
        analysis = Analysis(
            original_text=original_text,
            human_score=human_score,
            ai_score=ai_score,
            readability=metrics.get('readability_score', 0),
            emotional_variation=metrics.get('emotional_variation', 0),
            vocabulary_score=metrics.get('vocabulary_score', 0),
            sentence_complexity=metrics.get('sentence_complexity', 0),
            repetition_score=metrics.get('repetition_score', 0),
            formality_score=metrics.get('formality_score', 0),
            sentiment_label=metrics.get('sentiment_label', 'neutral'),
            sentence_count=metrics.get('sentence_count', 0),
            word_count=metrics.get('word_count', 0),
            avg_word_length=metrics.get('avg_word_length', 0),
            unique_words_ratio=metrics.get('unique_words_ratio', 0)
        )
        
        db.session.add(analysis)
        db.session.commit()
        
        return analysis
    
    @staticmethod
    def save_history(analysis_id, summary, report):
        """Save to history"""
        history = History(
            analysis_id=analysis_id,
            summary=summary,
            generated_report=report
        )
        
        db.session.add(history)
        db.session.commit()
        
        return history
    
    @staticmethod
    def get_all_analyses():
        """Get all analyses from database"""
        return Analysis.query.order_by(Analysis.created_at.desc()).all()
    
    @staticmethod
    def get_analysis(analysis_id):
        """Get single analysis"""
        return Analysis.query.get(analysis_id)
    
    @staticmethod
    def get_statistics():
        """Get overall statistics"""
        analyses = Analysis.query.all()
        
        if not analyses:
            return {
                'total': 0,
                'avg_human_score': 0,
                'avg_ai_score': 0,
                'avg_readability': 0
            }
        
        total = len(analyses)
        avg_human = sum(a.human_score for a in analyses) / total
        avg_ai = sum(a.ai_score for a in analyses) / total
        avg_readability = sum(a.readability for a in analyses) / total
        
        return {
            'total': total,
            'avg_human_score': round(avg_human, 2),
            'avg_ai_score': round(avg_ai, 2),
            'avg_readability': round(avg_readability, 2)
        }
