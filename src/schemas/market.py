from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

from .base import TimeframeEnum

class OHLCVBase(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

class OHLCVCreate(OHLCVBase):
    exchange_id: str
    symbol: str
    timeframe: TimeframeEnum
    additional_data: Dict[str, Any] = Field(default_factory=dict)

class OHLCVInDB(OHLCVCreate):
    id: int

    class Config:
        from_attributes = True

class OHLCV(OHLCVInDB):
    pass

class MarketDataFilter(BaseModel):
    exchange_id: str
    symbol: str
    timeframe: TimeframeEnum
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: Optional[int] = None
