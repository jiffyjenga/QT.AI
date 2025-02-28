from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

from .base import OrderTypeEnum, OrderSideEnum, OrderStatusEnum

class TradeBase(BaseModel):
    exchange_id: str
    symbol: str
    order_type: OrderTypeEnum
    side: OrderSideEnum
    quantity: float
    price: float
    cost: float = Field(..., description="Total cost of the trade (quantity * price + fees)")
    fee: float = 0.0
    status: OrderStatusEnum = OrderStatusEnum.OPEN
    notes: Optional[str] = None
    additional_data: Dict[str, Any] = Field(default_factory=dict)

class TradeCreate(TradeBase):
    strategy_id: Optional[int] = None
    order_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class TradeUpdate(BaseModel):
    order_id: Optional[str] = None
    status: Optional[OrderStatusEnum] = None
    profit_loss: Optional[float] = None
    profit_loss_pct: Optional[float] = None
    notes: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None

class TradeInDB(TradeBase):
    id: int
    user_id: int
    strategy_id: Optional[int] = None
    order_id: Optional[str] = None
    timestamp: datetime
    profit_loss: Optional[float] = None
    profit_loss_pct: Optional[float] = None

    class Config:
        from_attributes = True

class Trade(TradeInDB):
    pass

class TradeFilter(BaseModel):
    exchange_id: Optional[str] = None
    symbol: Optional[str] = None
    strategy_id: Optional[int] = None
    side: Optional[OrderSideEnum] = None
    status: Optional[OrderStatusEnum] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
