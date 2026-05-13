import numpy as np

class ScoringEngine:
    
    @staticmethod
    def calculate_scores(metrics):
        """
        Calculate human and AI scores based on text metrics.
        yaha actual scoring logic hai.
        """
        
        # Weights for different factors
        weights = {
            'vocabulary': 0.15,
            'repetition': 0.10,
            'sentence_variety': 0.15,
            'emotional_variation': 0.12,
            'readability': 0.10,
            'formality': 0.12,
            'punctuation': 0.08,
            'pronoun_usage': 0.08,
            'capitalization': 0.05,
            'complexity': 0.05
        }
        
        # Calculate individual scores (0-100, higher = more human-like)
        scores = {}
        
        # Vocabulary diversity - high diversity is more human-like
        scores['vocabulary'] = min(100, metrics.get('vocabulary_score', 0) * 1.2)
        
        # Repetition - low repetition is more human-like
        scores['repetition'] = 100 - min(100, metrics.get('repetition_score', 0))
        
        # Sentence variety - variance in sentence length is more human-like
        variance = metrics.get('sentence_length_variance', 0)
        scores['sentence_variety'] = min(100, (variance / 20) * 100)
        
        # Emotional variation - more emotional markers = more human
        scores['emotional_variation'] = metrics.get('emotional_variation', 0)
        
        # Readability - moderate readability is human-like (too simple or complex = AI)
        readability = metrics.get('readability_score', 50)
        if 30 <= readability <= 70:
            scores['readability'] = 100
        else:
            scores['readability'] = max(0, 100 - abs(readability - 50) * 2)
        
        # Formality - moderate formality is human-like
        formality = metrics.get('formality_score', 50)
        if 30 <= formality <= 70:
            scores['formality'] = 80
        else:
            scores['formality'] = max(0, 80 - abs(formality - 50))
        
        # Punctuation diversity - more punctuation variety = more human
        scores['punctuation'] = min(100, metrics.get('punctuation_diversity', 0) * 3)
        
        # Pronoun usage - natural pronoun usage = more human
        pronoun_ratio = metrics.get('pronoun_ratio', 0)
        if 5 <= pronoun_ratio <= 15:
            scores['pronoun_usage'] = 90
        elif pronoun_ratio < 5:
            scores['pronoun_usage'] = max(0, 70 - (5 - pronoun_ratio) * 5)
        else:
            scores['pronoun_usage'] = max(0, 70 - (pronoun_ratio - 15) * 3)
        
        # Capitalization - natural capitalization patterns
        cap_ratio = metrics.get('capitalization_ratio', 0)
        if 5 <= cap_ratio <= 12:
            scores['capitalization'] = 85
        else:
            scores['capitalization'] = max(0, 85 - abs(cap_ratio - 8.5) * 3)
        
        # Sentence complexity - moderate complexity is human-like
        complexity = metrics.get('sentence_complexity', 50)
        if 30 <= complexity <= 70:
            scores['complexity'] = 80
        else:
            scores['complexity'] = max(0, 80 - abs(complexity - 50))
        
        # Calculate weighted human score
        human_score = sum(scores[key] * weights[key] for key in weights)
        human_score = round(max(0, min(100, human_score)), 2)
        
        # AI score is inverse of human score (not 100-human_score, but adjusted)
        ai_score = round(max(0, min(100, 100 - human_score * 0.85)), 2)
        
        return {
            'human_score': human_score,
            'ai_score': ai_score,
            'score_breakdown': scores,
            'confidence': ScoringEngine._calculate_confidence(scores)
        }
    
    @staticmethod
    def _calculate_confidence(scores):
        """
        Calculate confidence in the scores.
        Scores are more confident when they're more consistent.
        """
        values = list(scores.values())
        if len(values) < 2:
            return 50
        
        mean = np.mean(values)
        variance = np.var(values)
        std_dev = np.sqrt(variance)
        
        # If scores are very consistent, confidence is higher
        cv = std_dev / mean if mean > 0 else 0
        confidence = max(50, 100 - (cv * 20))
        return round(min(100, confidence), 2)
