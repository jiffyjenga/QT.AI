# QT.AI - Advanced Multi-Asset Trading Bot

QT.AI is a sophisticated trading bot that leverages artificial intelligence and machine learning to execute trades across multiple asset classes and exchanges. It features advanced trading strategies, real-time market data analysis, and a comprehensive web dashboard.

## Features

- **Multi-Asset, Multi-Exchange Support**: Trade cryptocurrencies, stocks, forex, and commodities through a unified interface
- **Advanced Trading Strategies**: Implement scalping, arbitrage, trend-following, and high-frequency trading strategies
- **AI-Powered Analysis**: Utilize LSTM networks and reinforcement learning for price prediction and optimal trading decisions
- **Real-Time Market Sentiment**: Analyze news, social media, and on-chain data to gauge market sentiment
- **Risk Management**: Implement sophisticated risk management with position sizing, stop-loss mechanisms, and portfolio diversification
- **Web Dashboard**: Monitor and control your trading strategies through a comprehensive web interface

## Technology Stack

- **Backend**: Python with FastAPI for high-performance API endpoints
- **AI/ML**: TensorFlow and PyTorch for deep learning models
- **Data Processing**: Pandas and NumPy for data manipulation
- **Exchange Connectivity**: CCXT for unified exchange API access
- **Frontend**: React.js with modern UI components
- **Database**: SQLAlchemy with SQLite (development) / PostgreSQL (production)
- **Real-Time Updates**: WebSockets for live data streaming

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- Exchange API keys (for live trading)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/jiffyjenga/QT.AI.git
   cd QT.AI
   ```

2. Set up the Python environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Start the backend server:
   ```
   python -m src.main
   ```

5. Install frontend dependencies:
   ```
   cd frontend
   npm install
   ```

6. Start the frontend development server:
   ```
   npm run dev
   ```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## WebSocket API

The WebSocket API provides real-time market data. Connect to:
- ws://localhost:8000/ws/market

Example subscription message:
```json
{
  "type": "subscribe",
  "exchange": "binance",
  "symbol": "BTC/USDT",
  "channel": "ticker"
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [CCXT](https://github.com/ccxt/ccxt) for exchange connectivity
- [FastAPI](https://fastapi.tiangolo.com/) for the API framework
- [TensorFlow](https://www.tensorflow.org/) and [PyTorch](https://pytorch.org/) for ML capabilities
