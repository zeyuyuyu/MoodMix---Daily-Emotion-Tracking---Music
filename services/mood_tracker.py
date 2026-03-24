import pandas as pd
from textblob import TextBlob

class MoodTracker:
    def __init__(self):
        self.data = pd.DataFrame(columns=['date', 'mood', 'sentiment_score'])

    def log_mood(self, date, mood):
        text = f"I feel {mood} today."
        sentiment = TextBlob(text).sentiment.polarity
        self.data = self.data.append({'date': date, 'mood': mood, 'sentiment_score': sentiment}, ignore_index=True)

    def get_mood_history(self):
        return self.data

    def get_sentiment_analysis(self):
        return self.data['sentiment_score'].mean()
