"""
Data integration module for QT.AI trading bot.

This module combines market data, technical indicators, sentiment analysis,
and blockchain data to create a comprehensive dataset for AI models.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class DataIntegrator:
    """Data integrator for combining multiple data sources."""
    
    def __init__(self, market_data_service=None, news_analyzer=None, 
                 social_media_analyzer=None, blockchain_analyzer=None):
        """Initialize the data integrator."""
        self.market_data_service = market_data_service
        self.news_analyzer = news_analyzer
        self.social_media_analyzer = social_media_analyzer
        self.blockchain_analyzer = blockchain_analyzer
        logger.info("Initialized data integrator")
    
    def get_integrated_data(self, asset, asset_type="crypto", days_back=30, interval="1d"):
        """Get integrated data for an asset."""
        logger.info(f"Getting integrated data for {asset} ({asset_type})")
        
        # Get market data
        market_data = self._get_market_data(asset, asset_type, days_back, interval)
        if market_data.empty:
            logger.warning(f"No market data available for {asset}")
            return pd.DataFrame()
        
        # Add technical indicators
        market_data = self._add_technical_indicators(market_data)
        
        # Add sentiment data if available
        if self.news_analyzer:
            sentiment_data = self._get_news_sentiment(asset, asset_type, days_back)
            if not sentiment_data.empty:
                market_data = self._merge_sentiment_data(market_data, sentiment_data)
        
        # Add social media sentiment if available
        if self.social_media_analyzer:
            social_sentiment = self._get_social_sentiment(asset, asset_type, days_back)
            if not social_sentiment.empty:
                market_data = self._merge_social_sentiment(market_data, social_sentiment)
        
        # Add blockchain data if available and asset is crypto
        if self.blockchain_analyzer and asset_type == "crypto":
            blockchain_data = self._get_blockchain_data(asset, days_back)
            if not blockchain_data.empty:
                market_data = self._merge_blockchain_data(market_data, blockchain_data)
        
        logger.info(f"Integrated data shape: {market_data.shape}")
        return market_data
    
    def _get_market_data(self, asset, asset_type, days_back, interval):
        """Get market data for an asset."""
        if self.market_data_service:
            return self.market_data_service.get_historical_data(
                asset=asset, 
                asset_type=asset_type, 
                days_back=days_back, 
                interval=interval
            )
        else:
            logger.warning("No market data service available")
            return pd.DataFrame()
    
    def _add_technical_indicators(self, df):
        """Add technical indicators to market data."""
        if df.empty:
            return df
        
        # Make a copy to avoid modifying the original
        df = df.copy()
        
        # Simple Moving Averages
        df['sma_7'] = df['close'].rolling(window=7).mean()
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        
        # Exponential Moving Averages
        df['ema_12'] = df['close'].ewm(span=12, adjust=False).mean()
        df['ema_26'] = df['close'].ewm(span=26, adjust=False).mean()
        
        # MACD
        df['macd'] = df['ema_12'] - df['ema_26']
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']
        
        # Relative Strength Index (RSI)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['bb_middle'] = df['close'].rolling(window=20).mean()
        df['bb_std'] = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + 2 * df['bb_std']
        df['bb_lower'] = df['bb_middle'] - 2 * df['bb_std']
        
        # Volume indicators
        df['volume_sma_20'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma_20']
        
        # Fill NaN values
        df = df.fillna(method='bfill')
        
        return df
    
    def _get_news_sentiment(self, asset, asset_type, days_back):
        """Get news sentiment data for an asset."""
        if not self.news_analyzer:
            return pd.DataFrame()
        
        # Get news articles
        news_df = self.news_analyzer.get_asset_specific_news(
            asset=asset, 
            asset_type=asset_type, 
            days_back=days_back
        )
        
        if news_df.empty:
            return pd.DataFrame()
        
        # Analyze sentiment for each article
        sentiments = []
        for _, row in news_df.iterrows():
            title = row['title']
            description = row.get('description', '')
            content = row.get('content', '')
            
            # Combine text for sentiment analysis
            text = f"{title}. {description} {content}"
            sentiment = self.news_analyzer.analyze_sentiment(text)
            
            sentiments.append({
                'date': pd.to_datetime(row['publishedAt']).date(),
                'sentiment_score': sentiment['score'] if sentiment['label'] == 'POSITIVE' else -sentiment['score'] if sentiment['label'] == 'NEGATIVE' else 0,
                'source': row.get('source', {}).get('name', 'unknown')
            })
        
        # Create DataFrame and aggregate by date
        sentiment_df = pd.DataFrame(sentiments)
        if sentiment_df.empty:
            return pd.DataFrame()
        
        # Aggregate sentiment by date
        daily_sentiment = sentiment_df.groupby('date').agg({
            'sentiment_score': 'mean',
            'source': 'count'
        }).reset_index()
        
        daily_sentiment.rename(columns={'source': 'news_count'}, inplace=True)
        
        return daily_sentiment
    
    def _get_social_sentiment(self, asset, asset_type, days_back):
        """Get social media sentiment data for an asset."""
        if not self.social_media_analyzer:
            return pd.DataFrame()
        
        # This is a placeholder for the actual implementation
        # In a real implementation, this would fetch and process social media data
        
        # Create mock data
        dates = [datetime.now().date() - timedelta(days=i) for i in range(days_back)]
        sentiment_scores = np.random.normal(0.2, 0.3, days_back)  # Slightly positive bias
        mention_counts = np.random.randint(10, 1000, days_back)
        
        social_df = pd.DataFrame({
            'date': dates,
            'social_sentiment': sentiment_scores,
            'mention_count': mention_counts
        })
        
        return social_df
    
    def _get_blockchain_data(self, asset, days_back):
        """Get blockchain data for a cryptocurrency."""
        if not self.blockchain_analyzer:
            return pd.DataFrame()
        
        # Get network metrics
        network_df = self.blockchain_analyzer.get_network_metrics(asset=asset, days_back=days_back)
        
        # Get exchange flows
        flows_df = self.blockchain_analyzer.get_exchange_flows(asset=asset, days_back=min(days_back, 7))
        
        # Merge data
        if not network_df.empty and not flows_df.empty:
            blockchain_df = pd.merge(
                network_df, 
                flows_df, 
                on='date', 
                how='left'
            )
        elif not network_df.empty:
            blockchain_df = network_df
        elif not flows_df.empty:
            blockchain_df = flows_df
        else:
            return pd.DataFrame()
        
        return blockchain_df
    
    def _merge_sentiment_data(self, market_data, sentiment_data):
        """Merge sentiment data with market data."""
        if market_data.empty or sentiment_data.empty:
            return market_data
        
        # Ensure date column exists in market_data
        if 'date' not in market_data.columns:
            market_data['date'] = pd.to_datetime(market_data.index).date()
        
        # Merge data
        merged_df = pd.merge(
            market_data,
            sentiment_data,
            on='date',
            how='left'
        )
        
        # Fill NaN values
        merged_df['sentiment_score'] = merged_df['sentiment_score'].fillna(0)
        merged_df['news_count'] = merged_df['news_count'].fillna(0)
        
        return merged_df
    
    def _merge_social_sentiment(self, market_data, social_sentiment):
        """Merge social media sentiment with market data."""
        if market_data.empty or social_sentiment.empty:
            return market_data
        
        # Ensure date column exists in market_data
        if 'date' not in market_data.columns:
            market_data['date'] = pd.to_datetime(market_data.index).date()
        
        # Merge data
        merged_df = pd.merge(
            market_data,
            social_sentiment,
            on='date',
            how='left'
        )
        
        # Fill NaN values
        merged_df['social_sentiment'] = merged_df['social_sentiment'].fillna(0)
        merged_df['mention_count'] = merged_df['mention_count'].fillna(0)
        
        return merged_df
    
    def _merge_blockchain_data(self, market_data, blockchain_data):
        """Merge blockchain data with market data."""
        if market_data.empty or blockchain_data.empty:
            return market_data
        
        # Ensure date column exists in market_data
        if 'date' not in market_data.columns:
            market_data['date'] = pd.to_datetime(market_data.index).date()
        
        # Merge data
        merged_df = pd.merge(
            market_data,
            blockchain_data,
            on='date',
            how='left'
        )
        
        # Fill NaN values
        for col in blockchain_data.columns:
            if col != 'date' and col in merged_df.columns:
                merged_df[col] = merged_df[col].fillna(method='ffill').fillna(method='bfill')
        
        return merged_df
