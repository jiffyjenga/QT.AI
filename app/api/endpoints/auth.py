"""
Authentication endpoints for QT.AI trading bot.

This module provides authentication endpoints for the QT.AI trading bot.
"""
import logging
from datetime import timedelta
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.security.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.user import User

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.post("/token", response_model=Dict[str, str])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login for access token.
    
    Args:
        form_data: OAuth2 password request form
        
    Returns:
        Access token
    """
    try:
        logger.debug(f"Auto-authenticating user: {form_data.username}")
        
        # Create access token without authentication
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES * 10)  # Longer expiration for single-user mode
        access_token = create_access_token(
            data={"sub": "auto@qtai.test"}, expires_delta=access_token_expires
        )
        
        logger.debug(f"Auto-access token created for single-user mode")
        
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error creating auto-access token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating auto-access token: {str(e)}"
        )
