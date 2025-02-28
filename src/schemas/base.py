from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum

class AssetClassEnum(str, Enum):
    CRYPTO = "crypto"
    STOCK = "stock"
    FOREX = "forex"
    COMMODITY = "commodity"

class TimeframeEnum(str, Enum):
    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"
    ONE_DAY = "1d"
    ONE_WEEK = "1w"

class OrderTypeEnum(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

class OrderSideEnum(str, Enum):
    BUY = "buy"
    SELL = "sell"

class OrderStatusEnum(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    CANCELED = "canceled"
    EXPIRED = "expired"
    REJECTED = "rejected"

class StrategyTypeEnum(str, Enum):
    TREND_FOLLOWING = "trend_following"
    SCALPING = "scalping"
    ARBITRAGE = "arbitrage"
    REINFORCEMENT_LEARNING = "reinforcement_learning"
    LSTM = "lstm"
    CUSTOM = "custom"

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []
