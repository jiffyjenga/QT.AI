from pydantic import BaseModel
from typing import List, Optional, Tuple

class OHLCVResponse(BaseModel):
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float

class MarketSummary(BaseModel):
    symbol: str
    price: float
    change24h: float
    high24h: float
    low24h: float
    volume24h: float

class OrderBookResponse(BaseModel):
    symbol: str
    bids: List[Tuple[float, float]]  # [price, amount]
    asks: List[Tuple[float, float]]  # [price, amount]
    timestamp: int
