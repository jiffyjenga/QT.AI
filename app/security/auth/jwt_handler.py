"""
JWT Handler for authentication.

This module provides a simple JWT handler for testing.
"""
import logging
import jwt
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class JWTHandler:
    """Simple JWT handler for authentication."""
    
    def __init__(self, secret_key, algorithm="HS256"):
        """Initialize the JWT handler."""
        self.secret_key = secret_key
        self.algorithm = algorithm
        logger.info(f"Initialized JWT handler with algorithm {algorithm}")
        
    def create_access_token(self, data, expires_delta=None):
        """Create an access token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        logger.info(f"Creating access token for {data.get('sub', 'unknown')}")
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def decode_token(self, token):
        """Decode a token."""
        logger.info("Decoding token")
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
