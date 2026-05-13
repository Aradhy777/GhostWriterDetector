import os

class OpenAIService:
    
    def __init__(self):
        self.api_key = ''
        self.endpoint = ''
        self.deployment_name = ''
        self.initialized = False
        self.client = None
    
    def initialize(self, api_key=None, endpoint=None, deployment_name=None):
        """Initialize OpenAI client if credentials available"""
        self.api_key = (api_key or os.getenv('AZURE_OPENAI_API_KEY', '')).strip()
        self.endpoint = (endpoint or os.getenv('AZURE_OPENAI_ENDPOINT', '')).strip()
        self.deployment_name = (deployment_name or os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', '')).strip()

        if not self.api_key or not self.endpoint or not self.deployment_name:
            self.initialized = False
            return
        
        try:
            import openai
            openai.api_type = 'azure'
            openai.api_key = self.api_key
            openai.api_base = self.endpoint
            openai.api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2023-05-15')
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
                engine=self.deployment_name,
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
