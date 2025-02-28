"""
JWT handler for authentication.

This module provides functionality to create, validate, and refresh
JWT tokens for authentication.
"""
import os
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
import jwt
import logging

logger = logging.getLogger(__name__)

class JWTHandler:
    """Handler for JWT token creation and validation."""
    
    def __init__(self, 
                 secret_key: Optional[str] = None, 
                 algorithm: str = "HS256",
                 access_token_expire_minutes: int = 30,
                 refresh_token_expire_days: int = 7):
        """Initialize the JWT handler."""
        self.secret_key = secret_key or os.environ.get("JWT_SECRET_KEY")
        if not self.secret_key:
            logger.warning("No JWT secret key provided. Using a random key.")
            self.secret_key = os.urandom(32).hex()
        
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create an access token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire.timestamp(), "type": "access"})
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create a refresh token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire.timestamp(), "type": "refresh"})
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decode and validate a token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Check if token is expired
            if "exp" in payload and payload["exp"] < time.time():
                logger.warning("Token expired")
                return {}
            
            return payload
        
        except jwt.PyJWTError as e:
            logger.error(f"Error decoding token: {str(e)}")
            return {}
    
    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """Refresh an access token using a refresh token."""
        payload = self.decode_token(refresh_token)
        
        if not payload:
            logger.warning("Invalid refresh token")
            return None
        
        # Check if token is a refresh token
        if payload.get("type") != "refresh":
            logger.warning("Token is not a refresh token")
            return None
        
        # Create new access token
        new_payload = {k: v for k, v in payload.items() if k not in ["exp", "type"]}
        return self.create_access_token(new_payload)
