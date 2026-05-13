from datetime import datetime

from models import db

class Analysis(db.Model):
    __tablename__ = 'analysis'
    
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.Text, nullable=False)
    human_score = db.Column(db.Float, default=0.0)
    ai_score = db.Column(db.Float, default=0.0)
    readability = db.Column(db.Float, default=0.0)
    emotional_variation = db.Column(db.Float, default=0.0)
    vocabulary_score = db.Column(db.Float, default=0.0)
    sentence_complexity = db.Column(db.Float, default=0.0)
    repetition_score = db.Column(db.Float, default=0.0)
    formality_score = db.Column(db.Float, default=0.0)
    
    sentiment_label = db.Column(db.String(50))
    sentence_count = db.Column(db.Integer)
    word_count = db.Column(db.Integer)
    avg_word_length = db.Column(db.Float)
    unique_words_ratio = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    history = db.relationship(
        'History',
        back_populates='analysis',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'human_score': round(self.human_score, 2),
            'ai_score': round(self.ai_score, 2),
            'readability': round(self.readability, 2),
            'emotional_variation': round(self.emotional_variation, 2),
            'vocabulary_score': round(self.vocabulary_score, 2),
            'sentence_complexity': round(self.sentence_complexity, 2),
            'repetition_score': round(self.repetition_score, 2),
            'formality_score': round(self.formality_score, 2),
            'sentiment_label': self.sentiment_label,
            'sentence_count': self.sentence_count,
            'word_count': self.word_count,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
