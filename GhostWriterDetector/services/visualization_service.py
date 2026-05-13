import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from datetime import datetime
import json

class VisualizationService:
    
    def __init__(self):
        self.chart_dir = 'static/charts'
        os.makedirs(self.chart_dir, exist_ok=True)
        plt.style.use('dark_background')
    
    def create_authenticity_gauge(self, human_score, ai_score, analysis_id):
        """Create gauge chart for authenticity scores"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.patch.set_facecolor('#1a1a1a')
        
        # Human score gauge
        colors1 = ['#4CAF50' if human_score > 50 else '#FF6B6B']
        ax1.bar(['Human-like'], [human_score], color=colors1, width=0.5)
        ax1.set_ylim(0, 100)
        ax1.set_ylabel('Score (%)', fontsize=10)
        ax1.set_title('Human-like Writing', fontsize=12, fontweight='bold')
        ax1.text(0, human_score + 3, f'{human_score}%', ha='center', fontweight='bold')
        ax1.set_facecolor('#222222')
        
        # AI score gauge
        colors2 = ['#FF6B6B' if ai_score > 50 else '#4CAF50']
        ax2.bar(['AI-assisted'], [ai_score], color=colors2, width=0.5)
        ax2.set_ylim(0, 100)
        ax2.set_ylabel('Score (%)', fontsize=10)
        ax2.set_title('AI-assisted Writing', fontsize=12, fontweight='bold')
        ax2.text(0, ai_score + 3, f'{ai_score}%', ha='center', fontweight='bold')
        ax2.set_facecolor('#222222')
        
        filename = f'authenticity_{analysis_id}.png'
        filepath = os.path.join(self.chart_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, facecolor='#1a1a1a', dpi=80)
        plt.close()
        
        return filename
    
    def create_metrics_radar(self, metrics, analysis_id):
        """Create radar chart for metrics analysis"""
        from math import pi
        
        categories = [
            'Vocabulary',
            'Complexity',
            'Readability',
            'Emotional',
            'Repetition',
            'Formality'
        ]
        
        values = [
            metrics.get('vocabulary_score', 0),
            metrics.get('sentence_complexity', 0),
            metrics.get('readability_score', 0),
            metrics.get('emotional_variation', 0),
            100 - metrics.get('repetition_score', 0),
            metrics.get('formality_score', 0)
        ]
        
        N = len(categories)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        values += values[:1]
        angles += angles[:1]
        
        fig = plt.figure(figsize=(8, 8))
        fig.patch.set_facecolor('#1a1a1a')
        ax = fig.add_subplot(111, projection='polar')
        ax.set_facecolor('#222222')
        
        ax.plot(angles, values, 'o-', linewidth=2, color='#3498db')
        ax.fill(angles, values, alpha=0.25, color='#3498db')
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, size=9)
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.grid(True, linestyle='--', alpha=0.7)
        
        filename = f'metrics_radar_{analysis_id}.png'
        filepath = os.path.join(self.chart_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, facecolor='#1a1a1a', dpi=80)
        plt.close()
        
        return filename
    
    def create_sentence_analysis(self, sentences, analysis_id):
        """Analyze sentence lengths"""
        sent_lengths = [len(s.split()) for s in sentences[:30]]  # first 30 sentences
        
        fig, ax = plt.subplots(figsize=(12, 5))
        fig.patch.set_facecolor('#1a1a1a')
        
        ax.bar(range(len(sent_lengths)), sent_lengths, color='#2ecc71', alpha=0.7)
        ax.set_xlabel('Sentence Number', fontsize=10)
        ax.set_ylabel('Word Count', fontsize=10)
        ax.set_title('Sentence Length Variation', fontsize=12, fontweight='bold')
        ax.set_facecolor('#222222')
        ax.axhline(y=sum(sent_lengths)/len(sent_lengths), color='#e74c3c', 
                   linestyle='--', label='Average', linewidth=2)
        ax.legend()
        
        filename = f'sentence_analysis_{analysis_id}.png'
        filepath = os.path.join(self.chart_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, facecolor='#1a1a1a', dpi=80)
        plt.close()
        
        return filename
    
    def create_comparison_chart(self, analyses_data, analysis_id):
        """Create comparison chart for multiple analyses"""
        if len(analyses_data) < 2:
            return None
        
        ids = [a['id'] for a in analyses_data]
        human_scores = [a['human_score'] for a in analyses_data]
        ai_scores = [a['ai_score'] for a in analyses_data]
        
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('#1a1a1a')
        
        x = range(len(ids))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], human_scores, width, label='Human-like', color='#4CAF50', alpha=0.8)
        ax.bar([i + width/2 for i in x], ai_scores, width, label='AI-assisted', color='#FF6B6B', alpha=0.8)
        
        ax.set_xlabel('Analysis', fontsize=10)
        ax.set_ylabel('Score (%)', fontsize=10)
        ax.set_title('Analysis Comparison', fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([f'#{id}' for id in ids])
        ax.legend()
        ax.set_facecolor('#222222')
        ax.set_ylim(0, 100)
        
        filename = f'comparison_{analysis_id}.png'
        filepath = os.path.join(self.chart_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, facecolor='#1a1a1a', dpi=80)
        plt.close()
        
        return filename
