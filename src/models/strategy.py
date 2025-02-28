from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class StrategyBase(BaseModel):
    name: str
    description: str
    type: str
    assets: List[str]
    parameters: Dict[str, Any]
    is_active: bool

class StrategyCreate(StrategyBase):
    pass

class StrategyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    assets: Optional[List[str]] = None
    parameters: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class StrategyResponse(StrategyBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class StrategyPerformance(BaseModel):
    strategy_id: int
    strategy_name: str
    timeframe: str
    total_trades: int
    profitable_trades: int
    win_rate: float
    profit_loss: float
    avg_profit: float
    trades: List[Any]
