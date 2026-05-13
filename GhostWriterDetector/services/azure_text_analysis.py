import os

class AzureTextAnalysisService:
    
    def __init__(self):
        self.endpoint = ''
        self.key = ''
        self.initialized = False
        self.client = None
    
    def initialize(self, endpoint=None, key=None):
        """Initialize Azure service - checks if credentials are available"""
        self.endpoint = (endpoint or os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT', '')).strip()
        self.key = (key or os.getenv('AZURE_TEXT_ANALYTICS_API_KEY', '')).strip()

        if not self.endpoint or not self.key:
            self.initialized = False
            return
        
        try:
            from azure.ai.textanalytics import TextAnalyticsClient
            from azure.core.credentials import AzureKeyCredential
            
            self.client = TextAnalyticsClient(
                endpoint=self.endpoint,
                credential=AzureKeyCredential(self.key)
            )
            self.initialized = True
        except:
            self.initialized = False
    
    def analyze_sentiment(self, text):
        """
        Analyze sentiment - returns mock data if credentials not available
        """
        if not self.initialized:
            # Mock response
            return {
                'sentiment': 'positive',
                'positive': 0.7,
                'neutral': 0.2,
                'negative': 0.1
            }
        
        try:
            result = self.client.analyze_sentiment(text, language="en")
            return {
                'sentiment': result.sentiment,
                'positive': result.confidence_scores.positive,
                'neutral': result.confidence_scores.neutral,
                'negative': result.confidence_scores.negative
            }
        except:
            return {'sentiment': 'positive', 'positive': 0.7, 'neutral': 0.2, 'negative': 0.1}
    
    def extract_key_phrases(self, text):
        """
        Extract key phrases - returns mock if unavailable
        """
        if not self.initialized:
            # Return common phrases from text
            words = text.split()
            return words[:5] if len(words) > 5 else words
        
        try:
            result = self.client.extract_key_phrases(text, language="en")
            return list(result)
        except:
            words = text.split()
            return words[:5] if len(words) > 5 else words
