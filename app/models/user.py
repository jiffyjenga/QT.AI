from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class TwoFactorMethod(str, Enum):
    NONE = "none"
    APP = "app"
    SMS = "sms"
    EMAIL = "email"

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER
    two_factor_enabled: bool = False
    two_factor_method: TwoFactorMethod = TwoFactorMethod.NONE
    setup_completed: bool = False

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        return v

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    two_factor_enabled: Optional[bool] = None
    two_factor_method: Optional[TwoFactorMethod] = None
    setup_completed: Optional[bool] = None

class UserInDB(UserBase):
    id: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime

class User(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
