"""
News analysis module for QT.AI trading bot.

This module uses NewsAPI to fetch financial news and analyzes sentiment
using natural language processing techniques.
"""
import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from newsapi import NewsApiClient
from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class NewsAnalyzer:
    """News analyzer for sentiment analysis of financial news."""
    
    def __init__(self, api_key=None, sentiment_model="distilbert-base-uncased-finetuned-sst-2-english"):
        """Initialize the news analyzer."""
        self.api_key = api_key or os.environ.get("NEWS_API_KEY")
        if not self.api_key:
            logger.warning("No NewsAPI key provided. News analysis will not work.")
        else:
            self.newsapi = NewsApiClient(api_key=self.api_key)
        
        # Load sentiment analysis model
        self.sentiment_analyzer = pipeline("sentiment-analysis", model=sentiment_model)
        logger.info(f"Initialized news analyzer with sentiment model: {sentiment_model}")
    
    def get_financial_news(self, keywords=None, sources=None, days_back=1, language='en', page_size=100):
        """Get financial news articles."""
        if not self.api_key:
            logger.error("Cannot fetch news: No NewsAPI key provided")
            return pd.DataFrame()
        
        # Default financial news sources if none provided
        if sources is None:
            sources = 'bloomberg,financial-times,business-insider,cnbc,the-wall-street-journal'
        
        # Default keywords if none provided
        if keywords is None:
            keywords = 'finance,stock,market,crypto,bitcoin,ethereum'
        
        # Calculate date range
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days_back)
        
        try:
            # Fetch news articles
            articles = self.newsapi.get_everything(
                q=keywords,
                sources=sources,
                from_param=from_date.strftime('%Y-%m-%d'),
                to=to_date.strftime('%Y-%m-%d'),
                language=language,
                sort_by='publishedAt',
                page_size=page_size
            )
            
            # Convert to DataFrame
            if articles['status'] == 'ok' and articles['totalResults'] > 0:
                df = pd.DataFrame(articles['articles'])
                logger.info(f"Fetched {len(df)} news articles")
                return df
            else:
                logger.warning(f"No articles found for the given parameters: {keywords}, {sources}")
                return pd.DataFrame()
        
        except Exception as e:
            logger.error(f"Error fetching news: {str(e)}")
            return pd.DataFrame()
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of a text."""
        try:
            result = self.sentiment_analyzer(text)
            return result[0]
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return {"label": "NEUTRAL", "score": 0.5}
    
    def get_asset_specific_news(self, asset, asset_type='crypto', days_back=1):
        """Get news specific to an asset (e.g., Bitcoin, Tesla)."""
        keywords = asset
        if asset_type == 'crypto':
            keywords = f"{asset},cryptocurrency,crypto"
        elif asset_type == 'stock':
            keywords = f"{asset},stock,shares"
        
        return self.get_financial_news(keywords=keywords, days_back=days_back)
