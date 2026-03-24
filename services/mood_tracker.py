from datetime import datetime
from typing import Dict, List, Optional
import statistics

class MoodTracker:
    def __init__(self):
        self.mood_entries = []
        self.mood_scale = {
            'ecstatic': 5,
            'happy': 4,
            'neutral': 3,
            'sad': 2,
            'depressed': 1
        }

    def log_mood(self, mood: str, notes: str = '', timestamp: Optional[datetime] = None) -> Dict:
        """Log a new mood entry with optional notes"""
        if mood.lower() not in self.mood_scale:
            raise ValueError(f'Invalid mood. Must be one of {list(self.mood_scale.keys())}')
        
        entry = {
            'mood': mood.lower(),
            'mood_score': self.mood_scale[mood.lower()],
            'notes': notes,
            'timestamp': timestamp or datetime.now()
        }
        self.mood_entries.append(entry)
        return entry

    def get_mood_history(self, days: int = 7) -> List[Dict]:
        """Retrieve mood history for the specified number of days"""
        cutoff = datetime.now().timestamp() - (days * 86400)
        return [entry for entry in self.mood_entries 
                if entry['timestamp'].timestamp() > cutoff]

    def get_mood_stats(self, days: int = 7) -> Dict:
        """Calculate mood statistics over the specified period"""
        history = self.get_mood_history(days)
        if not history:
            return {
                'average_mood': None,
                'most_common_mood': None,
                'mood_variance': None
            }

        scores = [entry['mood_score'] for entry in history]
        moods = [entry['mood'] for entry in history]

        return {
            'average_mood': statistics.mean(scores),
            'most_common_mood': max(set(moods), key=moods.count),
            'mood_variance': statistics.variance(scores) if len(scores) > 1 else 0
        }

    def get_mood_trend(self, days: int = 7) -> str:
        """Analyze mood trend over time"""
        history = self.get_mood_history(days)
        if len(history) < 2:
            return 'Insufficient data'

        scores = [entry['mood_score'] for entry in history]
        first_half = statistics.mean(scores[:len(scores)//2])
        second_half = statistics.mean(scores[len(scores)//2:])

        if second_half > first_half:
            return 'Improving'
        elif second_half < first_half:
            return 'Declining'
        return 'Stable'
