import hashlib
from datetime import datetime

class Utilities:
    
    @staticmethod
    def generate_hash(text):
        """Generate hash of text"""
        return hashlib.sha256(text.encode()).hexdigest()[:8]
    
    @staticmethod
    def format_datetime(dt):
        """Format datetime for display"""
        if isinstance(dt, str):
            return dt
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def truncate_text(text, max_length=100):
        """Truncate text for display"""
        if len(text) > max_length:
            return text[:max_length] + "..."
        return text
    
    @staticmethod
    def get_reading_time(text):
        """Estimate reading time in minutes"""
        word_count = len(text.split())
        reading_speed = 200
        return max(1, round(word_count / reading_speed))
    
    @staticmethod
    def calculate_percentage(value, total):
        """Calculate percentage"""
        if total == 0:
            return 0
        return round((value / total) * 100, 2)
