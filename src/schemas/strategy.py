from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

from .base import AssetClassEnum, StrategyTypeEnum

class StrategyBase(BaseModel):
    name: str
    description: Optional[str] = None
    strategy_type: StrategyTypeEnum
    asset_class: AssetClassEnum
    parameters: Dict[str, Any] = Field(default_factory=dict)
    is_active: bool = False

class StrategyCreate(StrategyBase):
    pass

class StrategyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    strategy_type: Optional[StrategyTypeEnum] = None
    asset_class: Optional[AssetClassEnum] = None
    parameters: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class StrategyInDB(StrategyBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Strategy(StrategyInDB):
    pass

class StrategyPerformanceBase(BaseModel):
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    profit_loss: float = 0.0
    win_rate: float = 0.0
    sharpe_ratio: Optional[float] = None
    max_drawdown: Optional[float] = None
    volatility: Optional[float] = None
    additional_metrics: Dict[str, Any] = Field(default_factory=dict)

class StrategyPerformanceCreate(StrategyPerformanceBase):
    strategy_id: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StrategyPerformanceInDB(StrategyPerformanceBase):
    id: int
    strategy_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class StrategyPerformance(StrategyPerformanceInDB):
    pass

class StrategyWithPerformance(Strategy):
    performance: Optional[StrategyPerformance] = None
