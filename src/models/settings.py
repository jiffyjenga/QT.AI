from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RiskSettingsBase(BaseModel):
    max_position_size: float
    max_daily_loss: float
    max_drawdown: float
    stop_loss_percent: float
    take_profit_percent: float
    confirm_trades: bool

class RiskSettingsUpdate(BaseModel):
    max_position_size: Optional[float] = None
    max_daily_loss: Optional[float] = None
    max_drawdown: Optional[float] = None
    stop_loss_percent: Optional[float] = None
    take_profit_percent: Optional[float] = None
    confirm_trades: Optional[bool] = None

class RiskSettingsResponse(RiskSettingsBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class ApiKeyBase(BaseModel):
    exchange: str
    api_key: str
    api_secret: str

class ApiKeyCreate(ApiKeyBase):
    pass

class ApiKeyResponse(ApiKeyBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
