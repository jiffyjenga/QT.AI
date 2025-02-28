"""
Trading Brain module for QT.AI trading bot.

This module integrates all AI components (LSTM, RL, sentiment analysis)
to make trading decisions based on comprehensive market analysis.
"""
import os
import pandas as pd
import numpy as np
from datetime import datetime
import logging

from app.ai.models.lstm_model import LSTMPricePredictor
from app.ai.models.rl_agent import RLTradingAgent, TradingEnvironment
from app.ai.data.data_integrator import DataIntegrator

logger = logging.getLogger(__name__)

class TradingBrain:
    """Trading Brain that integrates all AI components for decision making."""
    
    def __init__(self, 
                 market_data_service=None,
                 news_analyzer=None,
                 social_media_analyzer=None,
                 blockchain_analyzer=None,
                 model_dir='models'):
        """Initialize the trading brain."""
        # Data services
        self.market_data_service = market_data_service
        self.news_analyzer = news_analyzer
        self.social_media_analyzer = social_media_analyzer
        self.blockchain_analyzer = blockchain_analyzer
        
        # Data integrator
        self.data_integrator = DataIntegrator(
            market_data_service=market_data_service,
            news_analyzer=news_analyzer,
            social_media_analyzer=social_media_analyzer,
            blockchain_analyzer=blockchain_analyzer
        )
        
        # AI models
        self.lstm_models = {}  # Asset -> LSTM model mapping
        self.rl_agents = {}    # Asset -> RL agent mapping
        
        # Model directory
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        
        logger.info("Initialized Trading Brain")
    
    def train_models(self, asset, asset_type="crypto", days_back=365, interval="1d"):
        """Train AI models for an asset."""
        logger.info(f"Training models for {asset} ({asset_type})")
        
        # Get integrated data
        data = self.data_integrator.get_integrated_data(
            asset=asset,
            asset_type=asset_type,
            days_back=days_back,
            interval=interval
        )
        
        if data.empty:
            logger.error(f"No data available for {asset}")
            return False
        
        # Train LSTM model
        lstm_model = self._train_lstm_model(asset, data)
        
        # Train RL agent
        rl_agent = self._train_rl_agent(asset, data)
        
        # Store models
        self.lstm_models[asset] = lstm_model
        self.rl_agents[asset] = rl_agent
        
        logger.info(f"Successfully trained models for {asset}")
        return True
    
    def _train_lstm_model(self, asset, data):
        """Train LSTM model for price prediction."""
        logger.info(f"Training LSTM model for {asset}")
        
        # Create model directory
        model_dir = os.path.join(self.model_dir, asset, 'lstm')
        os.makedirs(model_dir, exist_ok=True)
        
        # Initialize LSTM model
        lstm_model = LSTMPricePredictor(
            sequence_length=60,
            n_features=data.shape[1],
            n_lstm_units=50,
            n_lstm_layers=2,
            model_dir=model_dir
        )
        
        # Build and train model
        lstm_model.build_model()
        # In a real implementation, we would train the model here
        # lstm_model.train(data, epochs=50, batch_size=32)
        
        logger.info(f"LSTM model for {asset} ready")
        return lstm_model
    
    def _train_rl_agent(self, asset, data):
        """Train RL agent for trading policy optimization."""
        logger.info(f"Training RL agent for {asset}")
        
        # Create model directory
        model_dir = os.path.join(self.model_dir, asset, 'rl')
        os.makedirs(model_dir, exist_ok=True)
        
        # Initialize RL agent
        rl_agent = RLTradingAgent(
            algorithm='ppo',
            policy='MlpPolicy',
            model_dir=model_dir
        )
        
        # Create environment
        env = rl_agent.create_environment(data)
        
        # Build model
        rl_agent.build_model(env)
        
        # In a real implementation, we would train the model here
        # rl_agent.train(env, total_timesteps=100000)
        
        logger.info(f"RL agent for {asset} ready")
        return rl_agent
    
    def get_trading_signal(self, asset, asset_type="crypto"):
        """Get trading signal for an asset."""
        logger.info(f"Getting trading signal for {asset} ({asset_type})")
        
        # Get latest data
        latest_data = self.data_integrator.get_integrated_data(
            asset=asset,
            asset_type=asset_type,
            days_back=60,  # Need enough data for sequence
            interval="1d"
        )
        
        if latest_data.empty:
            logger.error(f"No data available for {asset}")
            return {
                "asset": asset,
                "signal": "HOLD",
                "confidence": 0.0,
                "timestamp": datetime.now()
            }
        
        # Get price prediction from LSTM
        price_prediction = self._get_price_prediction(asset, latest_data)
        
        # Get trading action from RL
        trading_action = self._get_trading_action(asset, latest_data)
        
        # Get sentiment signal
        sentiment_signal = self._get_sentiment_signal(asset, asset_type)
        
        # Combine signals
        combined_signal = self._combine_signals(
            price_prediction=price_prediction,
            trading_action=trading_action,
            sentiment_signal=sentiment_signal
        )
        
        logger.info(f"Trading signal for {asset}: {combined_signal['signal']} (confidence: {combined_signal['confidence']:.2f})")
        return combined_signal
    
    def _get_price_prediction(self, asset, data):
        """Get price prediction from LSTM model."""
        # Check if model exists
        if asset not in self.lstm_models:
            logger.warning(f"No LSTM model available for {asset}")
            return {
                "predicted_price": None,
                "current_price": data['close'].iloc[-1] if not data.empty else None,
                "predicted_change": 0.0,
                "confidence": 0.0
            }
        
        # In a real implementation, we would use the model to predict
        # For now, return a mock prediction
        current_price = data['close'].iloc[-1]
        predicted_price = current_price * (1 + np.random.normal(0.01, 0.02))  # Random prediction
        
        return {
            "predicted_price": predicted_price,
            "current_price": current_price,
            "predicted_change": (predicted_price - current_price) / current_price,
            "confidence": 0.7  # Mock confidence
        }
    
    def _get_trading_action(self, asset, data):
        """Get trading action from RL agent."""
        # Check if agent exists
        if asset not in self.rl_agents:
            logger.warning(f"No RL agent available for {asset}")
            return {
                "action": "HOLD",
                "confidence": 0.0
            }
        
        # In a real implementation, we would use the agent to predict
        # For now, return a mock action
        actions = ["BUY", "SELL", "HOLD"]
        action = np.random.choice(actions, p=[0.3, 0.3, 0.4])  # Random action with bias towards HOLD
        
        return {
            "action": action,
            "confidence": 0.6  # Mock confidence
        }
    
    def _get_sentiment_signal(self, asset, asset_type):
        """Get sentiment signal from news and social media."""
        sentiment_score = 0.0
        confidence = 0.0
        sources = []
        
        # Get news sentiment if available
        if self.news_analyzer:
            news_df = self.news_analyzer.get_asset_specific_news(
                asset=asset,
                asset_type=asset_type,
                days_back=1
            )
            
            if not news_df.empty:
                # Analyze sentiment
                sentiments = []
                for _, row in news_df.iterrows():
                    title = row['title']
                    description = row.get('description', '')
                    
                    # Analyze sentiment
                    sentiment = self.news_analyzer.analyze_sentiment(f"{title}. {description}")
                    sentiments.append(sentiment['score'] if sentiment['label'] == 'POSITIVE' else -sentiment['score'] if sentiment['label'] == 'NEGATIVE' else 0)
                
                if sentiments:
                    news_sentiment = np.mean(sentiments)
                    sentiment_score += news_sentiment
                    confidence += 0.5
                    sources.append("news")
        
        # Get social media sentiment if available
        if self.social_media_analyzer:
            social_sentiment = self.social_media_analyzer.get_asset_sentiment(
                asset=asset,
                asset_type=asset_type
            )
            
            if social_sentiment:
                sentiment_score += social_sentiment['sentiment_score']
                confidence += 0.3
                sources.append("social_media")
        
        # Normalize sentiment score and confidence
        if sources:
            sentiment_score /= len(sources)
            confidence /= len(sources)
            
            # Convert sentiment score to signal
            if sentiment_score > 0.2:
                signal = "BUY"
            elif sentiment_score < -0.2:
                signal = "SELL"
            else:
                signal = "HOLD"
        else:
            signal = "HOLD"
            confidence = 0.0
        
        return {
            "signal": signal,
            "sentiment_score": sentiment_score,
            "confidence": confidence,
            "sources": sources
        }
    
    def _combine_signals(self, price_prediction, trading_action, sentiment_signal):
        """Combine different signals into a final trading signal."""
        # Initialize weights
        weights = {
            "price_prediction": 0.4,
            "trading_action": 0.4,
            "sentiment": 0.2
        }
        
        # Convert price prediction to signal
        if price_prediction["predicted_change"] > 0.02:
            price_signal = "BUY"
        elif price_prediction["predicted_change"] < -0.02:
            price_signal = "SELL"
        else:
            price_signal = "HOLD"
        
        # Get signals
        signals = {
            "BUY": 0,
            "SELL": 0,
            "HOLD": 0
        }
        
        # Add weighted signals
        signals[price_signal] += weights["price_prediction"] * price_prediction["confidence"]
        signals[trading_action["action"]] += weights["trading_action"] * trading_action["confidence"]
        signals[sentiment_signal["signal"]] += weights["sentiment"] * sentiment_signal["confidence"]
        
        # Get final signal
        final_signal = max(signals, key=signals.get)
        confidence = signals[final_signal]
        
        return {
            "signal": final_signal,
            "confidence": confidence,
            "timestamp": datetime.now(),
            "details": {
                "price_prediction": price_prediction,
                "trading_action": trading_action,
                "sentiment": sentiment_signal
            }
        }
    
    def update_models(self, asset, asset_type="crypto", days_back=30):
        """Update AI models with new data."""
        logger.info(f"Updating models for {asset}")
        
        # Get new data
        new_data = self.data_integrator.get_integrated_data(
            asset=asset,
            asset_type=asset_type,
            days_back=days_back,
            interval="1d"
        )
        
        if new_data.empty:
            logger.error(f"No new data available for {asset}")
            return False
        
        # Update LSTM model if available
        if asset in self.lstm_models:
            # In a real implementation, we would update the model here
            logger.info(f"Updated LSTM model for {asset}")
        
        # Update RL agent if available
        if asset in self.rl_agents:
            # In a real implementation, we would update the agent here
            logger.info(f"Updated RL agent for {asset}")
        
        return True
