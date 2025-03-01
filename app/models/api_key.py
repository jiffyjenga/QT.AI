"""
API key model for QT.AI trading bot.

This module provides API key models for the QT.AI trading bot.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ApiKeyBase(BaseModel):
    """Base API key model."""
    exchange: str
    label: Optional[str] = None
    permissions: Optional[str] = "read"
    
    @validator('exchange')
    def exchange_must_be_valid(cls, v):
        """Validate exchange."""
        valid_exchanges = ["binance", "coinbase", "kraken", "kucoin", "ftx", "bybit", "huobi", "okex"]
        if v.lower() not in valid_exchanges:
            raise ValueError(f"Exchange must be one of: {', '.join(valid_exchanges)}")
        return v.lower()

class ApiKeyCreate(ApiKeyBase):
    """API key create model."""
    api_key: str
    api_secret: str
    
    @validator('api_key', 'api_secret')
    def value_cannot_be_empty(cls, v):
        """Validate API key and secret."""
        if not v or v.strip() == "":
            raise ValueError("Value cannot be empty")
        return v

class ApiKeyUpdate(BaseModel):
    """API key update model."""
    label: Optional[str] = None
    permissions: Optional[str] = None
    is_active: Optional[bool] = None

class ApiKey(ApiKeyBase):
    """API key model."""
    id: str
    user_id: str
    masked_key: str
    created_at: datetime
    updated_at: datetime
    last_used: Optional[datetime] = None
    is_active: bool = True
    
    class Config:
        """Pydantic model configuration."""
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ApiKeyInDB(ApiKey):
    """API key in database model."""
    encrypted_key: str
    encrypted_secret: str
    
    class Config:
        """Pydantic model configuration."""
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
