import ccxt
import asyncio
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MarketDataService:
    def __init__(self):
        # Initialize exchange clients
        self.exchanges = {
            "binance": ccxt.binance({
                'apiKey': os.getenv('BINANCE_API_KEY', ''),
                'secret': os.getenv('BINANCE_API_SECRET', ''),
                'enableRateLimit': True,
            }),
            "coinbase": ccxt.coinbasepro({
                'apiKey': os.getenv('COINBASE_API_KEY', ''),
                'secret': os.getenv('COINBASE_API_SECRET', ''),
                'enableRateLimit': True,
            }),
            # Add more exchanges as needed
        }
        
        # Default exchange
        self.default_exchange = "binance"
        
        # Mock data for development
        self.use_mock_data = os.getenv('USE_MOCK_DATA', 'False').lower() == 'true'
    
    async def get_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 100, since: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get OHLCV (Open, High, Low, Close, Volume) data for a symbol"""
        if self.use_mock_data:
            return self._get_mock_ohlcv(symbol, timeframe, limit)
        
        try:
            exchange = self.exchanges[self.default_exchange]
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
            
            # Convert to list of dictionaries
            result = []
            for candle in ohlcv:
                result.append({
                    "timestamp": candle[0],
                    "open": candle[1],
                    "high": candle[2],
                    "low": candle[3],
                    "close": candle[4],
                    "volume": candle[5]
                })
            
            return result
        except Exception as e:
            print(f"Error fetching OHLCV data: {e}")
            # Fallback to mock data if real data fetch fails
            return self._get_mock_ohlcv(symbol, timeframe, limit)
    
    async def get_ticker(self, symbol: str) -> Dict[str, Any]:
        """Get current ticker data for a symbol"""
        if self.use_mock_data:
            return self._get_mock_ticker(symbol)
        
        try:
            exchange = self.exchanges[self.default_exchange]
            ticker = exchange.fetch_ticker(symbol)
            return ticker
        except Exception as e:
            print(f"Error fetching ticker data: {e}")
            # Fallback to mock data if real data fetch fails
            return self._get_mock_ticker(symbol)
    
    async def get_order_book(self, symbol: str, limit: int = 20) -> Dict[str, Any]:
        """Get order book data for a symbol"""
        if self.use_mock_data:
            return self._get_mock_order_book(symbol, limit)
        
        try:
            exchange = self.exchanges[self.default_exchange]
            order_book = exchange.fetch_order_book(symbol, limit)
            
            return {
                "symbol": symbol,
                "bids": order_book['bids'],
                "asks": order_book['asks'],
                "timestamp": order_book['timestamp']
            }
        except Exception as e:
            print(f"Error fetching order book data: {e}")
            # Fallback to mock data if real data fetch fails
            return self._get_mock_order_book(symbol, limit)
    
    async def get_market_summaries(self, symbols: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Get market summaries for multiple symbols"""
        if self.use_mock_data:
            return self._get_mock_market_summaries(symbols)
        
        try:
            exchange = self.exchanges[self.default_exchange]
            
            # If no symbols provided, get all tickers
            if not symbols:
                tickers = exchange.fetch_tickers()
                symbols = list(tickers.keys())
            
            result = []
            for symbol in symbols:
                ticker = await self.get_ticker(symbol)
                
                # Extract relevant data
                summary = {
                    "symbol": symbol,
                    "price": ticker['last'],
                    "change24h": ticker['last'] - ticker['open'],
                    "high24h": ticker['high'],
                    "low24h": ticker['low'],
                    "volume24h": ticker['quoteVolume'] if 'quoteVolume' in ticker else ticker['volume']
                }
                
                result.append(summary)
            
            return result
        except Exception as e:
            print(f"Error fetching market summaries: {e}")
            # Fallback to mock data if real data fetch fails
            return self._get_mock_market_summaries(symbols)
    
    # Mock data methods for development
    def _get_mock_ohlcv(self, symbol: str, timeframe: str, limit: int) -> List[Dict[str, Any]]:
        """Generate mock OHLCV data for development"""
        result = []
        now = datetime.now()
        
        # Determine time interval based on timeframe
        if timeframe == '1m':
            interval = timedelta(minutes=1)
        elif timeframe == '5m':
            interval = timedelta(minutes=5)
        elif timeframe == '15m':
            interval = timedelta(minutes=15)
        elif timeframe == '1h':
            interval = timedelta(hours=1)
        elif timeframe == '4h':
            interval = timedelta(hours=4)
        elif timeframe == '1d':
            interval = timedelta(days=1)
        else:
            interval = timedelta(hours=1)  # Default to 1h
        
        # Generate random price data
        base_price = 10000 if 'BTC' in symbol else 1000 if 'ETH' in symbol else 100
        
        for i in range(limit):
            timestamp = int((now - interval * (limit - i)).timestamp() * 1000)
            
            # Generate random price with some trend
            price_change = np.random.normal(0, base_price * 0.01)
            if i > 0:
                prev_close = result[i-1]['close']
                open_price = prev_close
                close_price = prev_close + price_change
            else:
                open_price = base_price
                close_price = base_price + price_change
            
            high_price = max(open_price, close_price) + abs(np.random.normal(0, base_price * 0.005))
            low_price = min(open_price, close_price) - abs(np.random.normal(0, base_price * 0.005))
            volume = abs(np.random.normal(base_price * 10, base_price * 5))
            
            result.append({
                "timestamp": timestamp,
                "open": open_price,
                "high": high_price,
                "low": low_price,
                "close": close_price,
                "volume": volume
            })
        
        return result
    
    def _get_mock_ticker(self, symbol: str) -> Dict[str, Any]:
        """Generate mock ticker data for development"""
        base_price = 10000 if 'BTC' in symbol else 1000 if 'ETH' in symbol else 100
        
        # Generate random price with some variation
        last_price = base_price + np.random.normal(0, base_price * 0.01)
        open_price = last_price - np.random.normal(0, base_price * 0.02)
        high_price = max(last_price, open_price) + abs(np.random.normal(0, base_price * 0.005))
        low_price = min(last_price, open_price) - abs(np.random.normal(0, base_price * 0.005))
        volume = abs(np.random.normal(base_price * 10, base_price * 5))
        
        return {
            'symbol': symbol,
            'timestamp': int(datetime.now().timestamp() * 1000),
            'datetime': datetime.now().isoformat(),
            'high': high_price,
            'low': low_price,
            'bid': last_price - np.random.normal(0, base_price * 0.001),
            'ask': last_price + np.random.normal(0, base_price * 0.001),
            'vwap': last_price + np.random.normal(0, base_price * 0.002),
            'open': open_price,
            'last': last_price,
            'close': last_price,
            'previousClose': open_price,
            'change': last_price - open_price,
            'percentage': ((last_price - open_price) / open_price) * 100,
            'average': (high_price + low_price) / 2,
            'baseVolume': volume,
            'quoteVolume': volume * last_price,
        }
    
    def _get_mock_order_book(self, symbol: str, limit: int) -> Dict[str, Any]:
        """Generate mock order book data for development"""
        base_price = 10000 if 'BTC' in symbol else 1000 if 'ETH' in symbol else 100
        
        # Generate bids (buy orders) slightly below current price
        bids = []
        for i in range(limit):
            price = base_price * (1 - 0.001 * (i + 1) - np.random.random() * 0.001)
            amount = abs(np.random.normal(1, 0.5))
            bids.append([price, amount])
        
        # Generate asks (sell orders) slightly above current price
        asks = []
        for i in range(limit):
            price = base_price * (1 + 0.001 * (i + 1) + np.random.random() * 0.001)
            amount = abs(np.random.normal(1, 0.5))
            asks.append([price, amount])
        
        return {
            "symbol": symbol,
            "bids": bids,
            "asks": asks,
            "timestamp": int(datetime.now().timestamp() * 1000)
        }
    
    def _get_mock_market_summaries(self, symbols: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Generate mock market summaries for development"""
        if not symbols:
            symbols = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "ADA/USDT", "XRP/USDT"]
        
        result = []
        for symbol in symbols:
            ticker = self._get_mock_ticker(symbol)
            
            summary = {
                "symbol": symbol,
                "price": ticker['last'],
                "change24h": ticker['change'],
                "high24h": ticker['high'],
                "low24h": ticker['low'],
                "volume24h": ticker['quoteVolume']
            }
            
            result.append(summary)
        
        return result
