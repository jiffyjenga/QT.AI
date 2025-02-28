from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from src.database.config import get_db
from src.database.models import MarketData, User
from src.schemas.market import OHLCV, MarketDataFilter
from src.api.dependencies.auth import get_current_active_user
from src.data.market.ohlcv_fetcher import OHLCVFetcher

router = APIRouter()

@router.get("/ohlcv", response_model=List[OHLCV])
async def get_ohlcv_data(
    exchange_id: str = Query(..., description="Exchange ID (e.g., 'binance')"),
    symbol: str = Query(..., description="Trading pair symbol (e.g., 'BTC/USDT')"),
    timeframe: str = Query("1h", description="Timeframe (e.g., '1m', '5m', '1h', '1d')"),
    limit: Optional[int] = Query(100, description="Number of candles to fetch"),
    since: Optional[datetime] = Query(None, description="Start time for data"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get OHLCV (Open, High, Low, Close, Volume) data for a symbol.
    
    This endpoint fetches historical price data from the database or directly from the exchange if not available.
    """
    # Check if data is in the database
    query = db.query(MarketData).filter(
        MarketData.exchange_id == exchange_id,
        MarketData.symbol == symbol,
        MarketData.timeframe == timeframe
    )
    
    if since:
        query = query.filter(MarketData.timestamp >= since)
    
    # Order by timestamp and limit
    query = query.order_by(MarketData.timestamp.desc()).limit(limit)
    db_data = query.all()
    
    # If data is in the database, return it
    if db_data and len(db_data) == limit:
        return db_data
    
    # Otherwise, fetch from exchange
    try:
        # Convert since to milliseconds timestamp if provided
        since_ms = int(since.timestamp() * 1000) if since else None
        
        # Create OHLCV fetcher
        fetcher = OHLCVFetcher(exchange_id=exchange_id)
        
        # Fetch data
        ohlcv_data = await fetcher.fetch_ohlcv(
            symbol=symbol,
            timeframe=timeframe,
            since=since_ms,
            limit=limit
        )
        
        # Convert to OHLCV objects
        result = []
        for candle in ohlcv_data:
            timestamp, open_price, high, low, close, volume = candle
            
            # Convert timestamp from milliseconds to datetime
            dt = datetime.fromtimestamp(timestamp / 1000)
            
            # Create MarketData object
            market_data = MarketData(
                exchange_id=exchange_id,
                symbol=symbol,
                timeframe=timeframe,
                timestamp=dt,
                open=open_price,
                high=high,
                low=low,
                close=close,
                volume=volume
            )
            
            # Add to database
            db.add(market_data)
            result.append(market_data)
        
        # Commit to database
        db.commit()
        
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching OHLCV data: {str(e)}"
        )

@router.get("/exchanges", response_model=List[str])
async def get_available_exchanges(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a list of available exchanges.
    """
    # This is a simplified implementation
    # In a real application, this would be fetched from a configuration or database
    return [
        "binance", "coinbase", "kraken", "kucoin", "bitfinex",
        "bitstamp", "huobi", "okex", "bybit", "ftx"
    ]

@router.get("/symbols/{exchange_id}", response_model=List[str])
async def get_available_symbols(
    exchange_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a list of available symbols for an exchange.
    """
    try:
        # Create OHLCV fetcher
        fetcher = OHLCVFetcher(exchange_id=exchange_id)
        
        # Fetch markets
        markets = await fetcher.exchange.fetch_markets()
        
        # Extract symbols
        symbols = [market['symbol'] for market in markets]
        
        return symbols
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching symbols: {str(e)}"
        )
