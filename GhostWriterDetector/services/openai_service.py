import os

class OpenAIService:
    
    def __init__(self):
        self.api_key = ''
        self.initialized = False
        self.client = None
    
    def initialize(self, api_key=None):
        """Initialize OpenAI client if credentials available"""
        self.api_key = (api_key or os.getenv('OPENAI_API_KEY', '')).strip()

        if not self.api_key:
            self.initialized = False
            return
        
        try:
            import openai
            openai.api_key = self.api_key
            self.initialized = True
        except:
            self.initialized = False
    
    def get_writing_summary(self, text):
        """
        Get AI summary of writing style
        Returns mock data if API unavailable
        """
        if len(text) > 500:
            text = text[:500]
        
        if not self.initialized:
            return f"This text ({len(text)} chars) contains {len(text.split())} words and appears to be written in a professional tone."
        
        try:
            import openai
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "user",
                    "content": f"Summarize the writing style of this text in 1 sentence: {text}"
                }],
                temperature=0.3,
                max_tokens=100
            )
            return response.choices[0].message.content
        except:
            return f"Text summary: {len(text)} characters, {len(text.split())} words"
