import ccxt.async_support as ccxt
from typing import Dict, List, Any, Optional
import asyncio
import logging
import pandas as pd
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class OHLCVFetcher:
    """
    Fetches OHLCV (Open, High, Low, Close, Volume) data from exchanges.
    """
    
    def __init__(self, exchange_id: str, api_key: str = "", api_secret: str = ""):
        """
        Initialize the OHLCV fetcher.
        
        Args:
            exchange_id: The CCXT exchange ID (e.g., 'binance', 'coinbase', 'kraken')
            api_key: API key for the exchange
            api_secret: API secret for the exchange
        """
        self.exchange_id = exchange_id
        self.api_key = api_key
        self.api_secret = api_secret
        self._initialize_exchange()
    
    def _initialize_exchange(self):
        """Initialize the CCXT exchange."""
        try:
            exchange_class = getattr(ccxt, self.exchange_id)
            self.exchange = exchange_class({
                'apiKey': self.api_key,
                'secret': self.api_secret,
                'enableRateLimit': True,
            })
        except Exception as e:
            logger.error(f"Failed to initialize exchange {self.exchange_id}: {e}")
            raise
    
    async def fetch_ohlcv(self, symbol: str, timeframe: str = '1h', 
                         since: Optional[int] = None, limit: Optional[int] = None) -> List[List]:
        """
        Fetch OHLCV data from the exchange.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTC/USDT')
            timeframe: Timeframe for the candles (e.g., '1m', '5m', '1h', '1d')
            since: Timestamp in milliseconds for the start of the data
            limit: Maximum number of candles to fetch
            
        Returns:
            List of OHLCV candles [timestamp, open, high, low, close, volume]
        """
        try:
            # If since is not provided, default to 100 candles from now
            if since is None and limit is None:
                limit = 100
            
            # Fetch the OHLCV data
            ohlcv = await self.exchange.fetch_ohlcv(symbol, timeframe, since, limit)
            return ohlcv
        except Exception as e:
            logger.error(f"Error fetching OHLCV data for {symbol} from {self.exchange_id}: {e}")
            raise
        finally:
            await self._close_exchange()
    
    async def fetch_ohlcv_dataframe(self, symbol: str, timeframe: str = '1h',
                                  since: Optional[int] = None, limit: Optional[int] = None) -> pd.DataFrame:
        """
        Fetch OHLCV data and convert to pandas DataFrame.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTC/USDT')
            timeframe: Timeframe for the candles (e.g., '1m', '5m', '1h', '1d')
            since: Timestamp in milliseconds for the start of the data
            limit: Maximum number of candles to fetch
            
        Returns:
            DataFrame with OHLCV data
        """
        ohlcv = await self.fetch_ohlcv(symbol, timeframe, since, limit)
        
        # Convert to DataFrame
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        return df
    
    async def _close_exchange(self):
        """Close the exchange connection."""
        try:
            await self.exchange.close()
        except Exception as e:
            logger.error(f"Error closing exchange {self.exchange_id}: {e}")
