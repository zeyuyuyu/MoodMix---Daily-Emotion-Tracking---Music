from datetime import datetime, timedelta
from typing import Dict, List, Optional
import statistics

class MoodTracker:
    def __init__(self):
        self.mood_history: Dict[datetime, Dict] = {}
        self.mood_scale = {
            1: 'Very Low',
            2: 'Low',
            3: 'Neutral',
            4: 'Good',
            5: 'Excellent'
        }
        self.genre_recommendations = {
            'Very Low': ['upbeat pop', 'motivational', 'uplifting classical'],
            'Low': ['light jazz', 'acoustic', 'ambient'],
            'Neutral': ['indie rock', 'pop', 'electronic'],
            'Good': ['dance', 'rock', 'hip hop'],
            'Excellent': ['party hits', 'electronic dance', 'energetic rock']
        }

    def log_mood(self, rating: int, notes: str = '') -> bool:
        if rating not in self.mood_scale:
            return False
        
        self.mood_history[datetime.now()] = {
            'rating': rating,
            'mood_label': self.mood_scale[rating],
            'notes': notes
        }
        return True

    def get_mood_pattern(self, days: int = 7) -> Dict:
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_moods = [
            entry['rating'] for date, entry in self.mood_history.items()
            if date >= cutoff_date
        ]

        if not recent_moods:
            return {'pattern': 'insufficient_data'}

        avg_mood = statistics.mean(recent_moods)
        mood_trend = 'stable'
        
        if len(recent_moods) >= 3:
            if recent_moods[-1] > recent_moods[-2] > recent_moods[-3]:
                mood_trend = 'improving'
            elif recent_moods[-1] < recent_moods[-2] < recent_moods[-3]:
                mood_trend = 'declining'

        return {
            'average_mood': round(avg_mood, 2),
            'trend': mood_trend,
            'num_entries': len(recent_moods),
            'recommended_genres': self.get_music_recommendations(avg_mood)
        }

    def get_music_recommendations(self, mood_value: float) -> List[str]:
        if mood_value < 1.5:
            return self.genre_recommendations['Very Low']
        elif mood_value < 2.5:
            return self.genre_recommendations['Low']
        elif mood_value < 3.5:
            return self.genre_recommendations['Neutral']
        elif mood_value < 4.5:
            return self.genre_recommendations['Good']
        else:
            return self.genre_recommendations['Excellent']

    def get_mood_summary(self, days: int = 30) -> Dict:
        pattern = self.get_mood_pattern(days)
        cutoff_date = datetime.now() - timedelta(days=days)
        
        mood_distribution = {
            label: len([e for d, e in self.mood_history.items()
                       if e['mood_label'] == label and d >= cutoff_date])
            for label in self.mood_scale.values()
        }

        return {
            'pattern_analysis': pattern,
            'mood_distribution': mood_distribution,
            'period_days': days
        }
