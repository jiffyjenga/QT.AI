from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum
from decimal import Decimal

class AssetType(str, Enum):
    CRYPTO = "crypto"
    STOCK = "stock"
    FOREX = "forex"
    COMMODITY = "commodity"

class AccountBase(BaseModel):
    user_id: str
    total_balance: Decimal = Field(default=Decimal('0.00'), ge=0)
    available_balance: Decimal = Field(default=Decimal('0.00'), ge=0)
    allocated_balance: Decimal = Field(default=Decimal('0.00'), ge=0)
    currency: str = "USD"
    
    @validator('available_balance')
    def available_balance_valid(cls, v, values):
        if 'total_balance' in values and v > values['total_balance']:
            raise ValueError('Available balance cannot exceed total balance')
        return v
    
    @validator('allocated_balance')
    def allocated_balance_valid(cls, v, values):
        if 'total_balance' in values and v > values['total_balance']:
            raise ValueError('Allocated balance cannot exceed total balance')
        return v

class AccountCreate(AccountBase):
    initial_deposit: Decimal = Field(default=Decimal('0.00'), ge=0)
    
    @validator('initial_deposit')
    def initial_deposit_valid(cls, v):
        if v < 0:
            raise ValueError('Initial deposit cannot be negative')
        return v

class AccountUpdate(BaseModel):
    total_balance: Optional[Decimal] = None
    available_balance: Optional[Decimal] = None
    allocated_balance: Optional[Decimal] = None
    currency: Optional[str] = None

class AccountTransaction(BaseModel):
    account_id: str
    amount: Decimal
    transaction_type: str  # deposit, withdrawal, allocation
    asset_type: Optional[AssetType] = None
    asset_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = "completed"
    notes: Optional[str] = None

class AccountInDB(AccountBase):
    id: str
    created_at: datetime
    updated_at: datetime
    transactions: List[AccountTransaction] = []

class Account(AccountBase):
    id: str
    created_at: datetime
    updated_at: datetime
