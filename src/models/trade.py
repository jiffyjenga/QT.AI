from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TradeBase(BaseModel):
    symbol: str
    type: str  # BUY or SELL
    amount: float
    price: float
    exchange: str

class TradeCreate(TradeBase):
    strategy_id: Optional[int] = None

class TradeResponse(TradeBase):
    id: int
    value: float
    fee: float
    status: str
    order_id: Optional[str] = None
    user_id: int
    strategy_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class TradeHistoryParams(BaseModel):
    limit: Optional[int] = 50
    offset: Optional[int] = 0
    symbol: Optional[str] = None
    strategy_id: Optional[int] = None
    type: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class TradeHistoryResponse(BaseModel):
    trades: List[TradeResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
