from importer import SentimentIntensityAnalyzer

def analyze_sentiment_vader(text):
    """Analyze the sentiment of the given text."""
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)
    if sentiment_score['compound'] > 0.05:
        sentiment = "POSITIVE"
    elif sentiment_score['compound'] < -0.05:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"
    return sentiment, sentiment_score