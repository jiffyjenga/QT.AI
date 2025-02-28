from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

from .base import Token

class UserBase(BaseModel):
    email: EmailStr
    username: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    id: int
    is_superuser: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class User(UserInDB):
    pass

class UserLogin(BaseModel):
    username: str
    password: str

class UserWithToken(BaseModel):
    user: User
    token: Token
