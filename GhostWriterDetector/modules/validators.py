import re

class Validators:
    
    @staticmethod
    def validate_text(text, min_length=20, max_length=50000):
        """
        Validate text input
        Basic validation
        """
        if not text:
            return False, "Text cannot be empty"
        
        text = text.strip()
        
        if len(text) < min_length:
            return False, f"Text must be at least {min_length} characters"
        
        if len(text) > max_length:
            return False, f"Text cannot exceed {max_length} characters"
        
        return True, None
    
    @staticmethod
    def validate_file_upload(filename):
        """Validate file upload"""
        allowed = {'txt', 'pdf'}
        
        if '.' not in filename:
            return False, "File has no extension"
        
        ext = filename.rsplit('.', 1)[1].lower()
        if ext not in allowed:
            return False, f"Only {', '.join(allowed)} files allowed"
        
        return True, None
    
    @staticmethod
    def is_valid_email(email):
        """Check if email is valid"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
