"""
Sentiment Analyzer for market sentiment analysis.

This module provides a simple sentiment analyzer for testing.
"""
import logging
import random

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Simple sentiment analyzer for market sentiment analysis."""
    
    def __init__(self):
        """Initialize the sentiment analyzer."""
        logger.info("Initialized sentiment analyzer")
        
    def analyze_text(self, text):
        """Analyze the sentiment of a text."""
        # For testing, just return a random sentiment
        logger.info(f"Analyzing sentiment of text: {text[:50]}...")
        return {
            "sentiment": random.choice(["positive", "neutral", "negative"]),
            "score": random.uniform(-1, 1)
        }
    
    def analyze_news(self, news_items):
        """Analyze the sentiment of news items."""
        # For testing, just return random sentiments
        logger.info(f"Analyzing sentiment of {len(news_items)} news items")
        return [
            {
                "title": item.get("title", ""),
                "sentiment": random.choice(["positive", "neutral", "negative"]),
                "score": random.uniform(-1, 1)
            }
            for item in news_items
        ]
