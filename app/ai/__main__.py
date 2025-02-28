"""
Main entry point for the AI module.

This module provides a command-line interface for training and testing
the AI models for the QT.AI trading bot.
"""
import os
import argparse
import logging
from datetime import datetime

from app.ai.trading_brain import TradingBrain
from app.ai.sentiment.news_analyzer import NewsAnalyzer
from app.ai.sentiment.social_media_analyzer import SocialMediaAnalyzer
from app.ai.data.blockchain_analyzer import BlockchainAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_trading_brain():
    """Set up the trading brain with all components."""
    # Initialize analyzers
    news_analyzer = NewsAnalyzer(api_key=os.environ.get("NEWS_API_KEY"))
    social_media_analyzer = SocialMediaAnalyzer()
    blockchain_analyzer = BlockchainAnalyzer(
        etherscan_api_key=os.environ.get("ETHERSCAN_API_KEY"),
        glassnode_api_key=os.environ.get("GLASSNODE_API_KEY")
    )
    
    # Initialize trading brain
    trading_brain = TradingBrain(
        news_analyzer=news_analyzer,
        social_media_analyzer=social_media_analyzer,
        blockchain_analyzer=blockchain_analyzer
    )
    
    return trading_brain

def train_models(args):
    """Train AI models for an asset."""
    trading_brain = setup_trading_brain()
    
    logger.info(f"Training models for {args.asset} ({args.asset_type})")
    success = trading_brain.train_models(
        asset=args.asset,
        asset_type=args.asset_type,
        days_back=args.days_back,
        interval=args.interval
    )
    
    if success:
        logger.info(f"Successfully trained models for {args.asset}")
    else:
        logger.error(f"Failed to train models for {args.asset}")

def get_signal(args):
    """Get trading signal for an asset."""
    trading_brain = setup_trading_brain()
    
    logger.info(f"Getting trading signal for {args.asset} ({args.asset_type})")
    signal = trading_brain.get_trading_signal(
        asset=args.asset,
        asset_type=args.asset_type
    )
    
    print(f"\nTrading Signal for {args.asset}:")
    print(f"Signal: {signal['signal']}")
    print(f"Confidence: {signal['confidence']:.2f}")
    print(f"Timestamp: {signal['timestamp']}")
    
    if args.verbose:
        print("\nDetails:")
        print(f"Price Prediction: {signal['details']['price_prediction']}")
        print(f"Trading Action: {signal['details']['trading_action']}")
        print(f"Sentiment: {signal['details']['sentiment']}")

def update_models(args):
    """Update AI models for an asset."""
    trading_brain = setup_trading_brain()
    
    logger.info(f"Updating models for {args.asset} ({args.asset_type})")
    success = trading_brain.update_models(
        asset=args.asset,
        asset_type=args.asset_type,
        days_back=args.days_back
    )
    
    if success:
        logger.info(f"Successfully updated models for {args.asset}")
    else:
        logger.error(f"Failed to update models for {args.asset}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="QT.AI Trading Bot - AI Module")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Train models command
    train_parser = subparsers.add_parser("train", help="Train AI models")
    train_parser.add_argument("--asset", type=str, required=True, help="Asset to train models for")
    train_parser.add_argument("--asset-type", type=str, default="crypto", choices=["crypto", "stock", "forex", "commodity"], help="Type of asset")
    train_parser.add_argument("--days-back", type=int, default=365, help="Days of historical data to use")
    train_parser.add_argument("--interval", type=str, default="1d", choices=["1m", "5m", "15m", "30m", "1h", "4h", "1d"], help="Data interval")
    
    # Get signal command
    signal_parser = subparsers.add_parser("signal", help="Get trading signal")
    signal_parser.add_argument("--asset", type=str, required=True, help="Asset to get signal for")
    signal_parser.add_argument("--asset-type", type=str, default="crypto", choices=["crypto", "stock", "forex", "commodity"], help="Type of asset")
    signal_parser.add_argument("--verbose", action="store_true", help="Show detailed signal information")
    
    # Update models command
    update_parser = subparsers.add_parser("update", help="Update AI models")
    update_parser.add_argument("--asset", type=str, required=True, help="Asset to update models for")
    update_parser.add_argument("--asset-type", type=str, default="crypto", choices=["crypto", "stock", "forex", "commodity"], help="Type of asset")
    update_parser.add_argument("--days-back", type=int, default=30, help="Days of new data to use")
    
    args = parser.parse_args()
    
    if args.command == "train":
        train_models(args)
    elif args.command == "signal":
        get_signal(args)
    elif args.command == "update":
        update_models(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
