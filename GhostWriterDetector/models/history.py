from datetime import datetime

from models import db

class History(db.Model):
    __tablename__ = 'history'
    
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'), nullable=False)
    summary = db.Column(db.Text)
    generated_report = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    analysis = db.relationship('Analysis', back_populates='history')
    
    def to_dict(self):
        return {
            'id': self.id,
            'analysis_id': self.analysis_id,
            'summary': self.summary,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
