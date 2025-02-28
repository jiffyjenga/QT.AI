from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from database.session import get_db
from utils.security import get_current_active_user
from services.market_service import MarketDataService
from models.market import OHLCVResponse, MarketSummary, OrderBookResponse

router = APIRouter()
market_service = MarketDataService()

@router.get("/ohlcv", response_model=List[OHLCVResponse])
async def get_ohlcv_data(
    symbol: str = Query(..., description="Trading pair symbol (e.g. BTC/USD)"),
    timeframe: str = Query("1h", description="Timeframe (e.g. 1m, 5m, 15m, 1h, 4h, 1d)"),
    limit: int = Query(100, description="Number of candles to return"),
    since: Optional[int] = Query(None, description="Timestamp in milliseconds to start from"),
    current_user = Depends(get_current_active_user),
):
    try:
        data = await market_service.get_ohlcv(symbol, timeframe, limit, since)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/summaries", response_model=List[MarketSummary])
async def get_market_summaries(
    symbols: Optional[str] = Query(None, description="Comma-separated list of symbols (e.g. BTC/USD,ETH/USD)"),
    current_user = Depends(get_current_active_user),
):
    try:
        symbol_list = symbols.split(",") if symbols else None
        data = await market_service.get_market_summaries(symbol_list)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/ticker/{symbol}", response_model=dict)
async def get_ticker(
    symbol: str,
    current_user = Depends(get_current_active_user),
):
    try:
        data = await market_service.get_ticker(symbol)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/orderbook/{symbol}", response_model=OrderBookResponse)
async def get_order_book(
    symbol: str,
    limit: int = Query(20, description="Number of orders to return on each side"),
    current_user = Depends(get_current_active_user),
):
    try:
        data = await market_service.get_order_book(symbol, limit)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
