"""
Test script for local testing.

This script tests the AI and security features of the QT.AI trading bot.
"""
import logging
import numpy as np
from app.ai.models.lstm_model import LSTMModel
from app.ai.sentiment.sentiment_analyzer import SentimentAnalyzer
from app.security.encryption.key_manager import KeyManager
from app.security.auth.jwt_handler import JWTHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_lstm_model():
    """Test the LSTM model."""
    logger.info("Testing LSTM model")
    model = LSTMModel(input_dim=5, hidden_dim=64, output_dim=1)
    data = np.random.normal(0, 1, (100, 5))
    predictions = model.predict(data)
    logger.info(f"Predictions shape: {predictions.shape}")
    
    # Train the model
    X_train = np.random.normal(0, 1, (1000, 10, 5))
    y_train = np.random.normal(0, 1, (1000, 1))
    history = model.train(X_train, y_train, epochs=5, batch_size=32)
    logger.info(f"Training history: {history}")
    
    return True

def test_sentiment_analyzer():
    """Test the sentiment analyzer."""
    logger.info("Testing sentiment analyzer")
    analyzer = SentimentAnalyzer()
    
    # Test text analysis
    text = "The market is looking very bullish today with strong momentum."
    sentiment = analyzer.analyze_text(text)
    logger.info(f"Sentiment: {sentiment}")
    
    # Test news analysis
    news_items = [
        {"title": "Bitcoin surges to new all-time high", "content": "Bitcoin has reached a new all-time high of $100,000."},
        {"title": "Stock market crashes amid recession fears", "content": "The stock market has crashed due to fears of a recession."},
        {"title": "Fed announces interest rate hike", "content": "The Federal Reserve has announced an interest rate hike of 0.25%."}
    ]
    sentiments = analyzer.analyze_news(news_items)
    logger.info(f"News sentiments: {sentiments}")
    
    return True

def test_key_manager():
    """Test the key manager."""
    logger.info("Testing key manager")
    manager = KeyManager("secure_password")
    
    # Test encryption and decryption
    api_key = "my_secret_api_key"
    encrypted = manager.encrypt_api_key(api_key)
    logger.info(f"Encrypted API key: {encrypted}")
    
    decrypted = manager.decrypt_api_key(encrypted)
    logger.info(f"Decrypted API key: {decrypted}")
    
    assert decrypted == api_key, "Decryption failed"
    
    return True

def test_jwt_handler():
    """Test the JWT handler."""
    logger.info("Testing JWT handler")
    handler = JWTHandler("secret_key")
    
    # Test token creation and decoding
    data = {"sub": "user@example.com", "role": "admin"}
    token = handler.create_access_token(data)
    logger.info(f"Access token: {token}")
    
    decoded = handler.decode_token(token)
    logger.info(f"Decoded token: {decoded}")
    
    assert decoded["sub"] == data["sub"], "Token decoding failed"
    assert decoded["role"] == data["role"], "Token decoding failed"
    
    return True

def main():
    """Run all tests."""
    logger.info("Starting local tests")
    
    tests = [
        ("LSTM Model", test_lstm_model),
        ("Sentiment Analyzer", test_sentiment_analyzer),
        ("Key Manager", test_key_manager),
        ("JWT Handler", test_jwt_handler)
    ]
    
    results = []
    for name, test_func in tests:
        logger.info(f"Running test: {name}")
        try:
            result = test_func()
            results.append((name, result))
            logger.info(f"Test {name} {'passed' if result else 'failed'}")
        except Exception as e:
            logger.error(f"Test {name} failed with error: {e}")
            results.append((name, False))
    
    # Print summary
    logger.info("Test summary:")
    for name, result in results:
        logger.info(f"  {name}: {'PASSED' if result else 'FAILED'}")
    
    all_passed = all(result for _, result in results)
    logger.info(f"All tests {'passed' if all_passed else 'failed'}")
    
    return all_passed

if __name__ == "__main__":
    main()
