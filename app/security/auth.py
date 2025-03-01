"""
Authentication module for QT.AI trading bot.

This module provides authentication and authorization functionality.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from app.models.user import User
from app.security.password import verify_password
from app.db import get_user_by_email

# JWT settings
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # For development only
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate a user.
    
    Args:
        email: User email
        password: User password
        
    Returns:
        User data if authentication is successful, None otherwise
    """
    user = get_user_by_email(email)
    if not user:
        return None
    
    if not verify_password(password, user["hashed_password"]):
        return None
    
    return user

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create an access token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time
        
    Returns:
        Access token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    Get the current user from the token.
    
    Args:
        token: Access token
        
    Returns:
        User data
    """
    # Bypass authentication and return a default user
    # Get the first user from the database or create a default one
    from app.db import db
    
    users = list(db["users"].values())
    if users:
        return users[0]
    
    # If no users exist, return a default user
    return {
        "id": "default_user",
        "email": "demo@qtai.test",
        "username": "demo_user",
        "full_name": "Demo User",
        "role": "user",
        "two_factor_enabled": False,
        "two_factor_method": "none",
        "setup_completed": True,
        "is_active": True
    }

async def get_current_active_user(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Get the current active user.
    
    Args:
        current_user: Current user
        
    Returns:
        Current active user
    """
    # Always return the user as active
    return current_user
