import re
import string
from collections import Counter
import textstat
import numpy as np

class TextProcessor:
    
    @staticmethod
    def preprocess_text(text):
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    @staticmethod
    def analyze_text(text):
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        words = text.split()
        
        if not words or not sentences:
            return {}
        
        # Basic metrics
        word_count = len(words)
        sentence_count = len(sentences)
        char_count = len(text)
        unique_words = len(set(w.lower() for w in words))
        
        # Sentence metrics
        sentence_lengths = [len(s.split()) for s in sentences]
        avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths)
        sentence_length_variance = np.var(sentence_lengths) if len(sentence_lengths) > 1 else 0
        
        # Word metrics
        word_lengths = [len(w) for w in words]
        avg_word_length = sum(word_lengths) / len(word_lengths)
        
        # Readability metrics
        flesch_kincaid = textstat.flesch_kincaid_grade(text)
        flesch_reading_ease = textstat.flesch_reading_ease(text)
        readability_score = max(0, min(100, (flesch_reading_ease / 100) * 100))
        
        # Vocabulary richness
        vocabulary_score = (unique_words / word_count * 100) if word_count > 0 else 0
        vocabulary_score = min(100, vocabulary_score)
        
        # Repetition analysis
        word_freq = Counter(w.lower().strip(string.punctuation) for w in words)
        most_common = word_freq.most_common(10)
        repetition_score = 0
        if most_common:
            high_freq_count = sum(1 for _, freq in most_common if freq > 3)
            repetition_score = (high_freq_count / 10) * 100
        
        # Punctuation diversity
        punctuation_marks = ''.join(c for c in text if c in string.punctuation)
        punct_types = len(set(punctuation_marks)) if punctuation_marks else 0
        punctuation_diversity = (punct_types / len(string.punctuation)) * 100
        
        # Sentence complexity (based on average length)
        sentence_complexity = min(100, (avg_sentence_length / 25) * 100)
        
        # Formality score (based on average word length)
        formality_score = min(100, (avg_word_length / 8) * 100)
        
        # Capitalization patterns
        capital_count = sum(1 for c in text if c.isupper())
        capitalization_ratio = (capital_count / len(text)) * 100 if text else 0
        
        # Emotional variation (pronoun usage, exclamation marks)
        pronouns = ['i', 'me', 'we', 'us', 'you', 'he', 'she', 'it', 'they']
        pronoun_count = sum(1 for w in [word.lower().strip(string.punctuation) for word in words] if w in pronouns)
        pronoun_ratio = (pronoun_count / word_count * 100) if word_count > 0 else 0
        
        exclamation_count = text.count('!')
        question_count = text.count('?')
        emotional_markers = exclamation_count + (question_count * 0.5)
        emotional_variation = min(100, (emotional_markers / sentence_count * 100) if sentence_count > 0 else 0)
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'char_count': char_count,
            'unique_words': unique_words,
            'unique_words_ratio': (unique_words / word_count * 100) if word_count > 0 else 0,
            'avg_sentence_length': round(avg_sentence_length, 2),
            'avg_word_length': round(avg_word_length, 2),
            'sentence_length_variance': round(sentence_length_variance, 2),
            'readability_score': round(readability_score, 2),
            'vocabulary_score': round(vocabulary_score, 2),
            'repetition_score': round(repetition_score, 2),
            'punctuation_diversity': round(punctuation_diversity, 2),
            'sentence_complexity': round(sentence_complexity, 2),
            'formality_score': round(formality_score, 2),
            'capitalization_ratio': round(capitalization_ratio, 2),
            'emotional_variation': round(emotional_variation, 2),
            'pronoun_ratio': round(pronoun_ratio, 2),
            'flesch_kincaid_grade': round(flesch_kincaid, 2),
            'flesch_reading_ease': round(flesch_reading_ease, 2)
        }
    
    @staticmethod
    def get_word_frequency(text, top_n=10):
        words = text.lower().split()
        clean_words = [w.strip(string.punctuation) for w in words if w.strip(string.punctuation)]
        word_freq = Counter(clean_words)
        return word_freq.most_common(top_n)
