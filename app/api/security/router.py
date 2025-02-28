"""
Security API router for QT.AI trading bot.

This module provides API endpoints for security features, including
user authentication, API key management, and compliance checks.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
import logging

from app.security.auth.jwt_handler import JWTHandler
from app.security.auth.two_factor import TwoFactorAuth
from app.security.auth.user_model import User, UserRole, Permission
from app.security.encryption.key_manager import KeyManager
from app.security.compliance.blockchain_analyzer import BlockchainAnalyzer

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/security", tags=["security"])

# OAuth2 scheme for JWT token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="security/token")

# Initialize security components
jwt_handler = JWTHandler(secret_key=os.environ.get("JWT_SECRET_KEY"))
two_factor_auth = TwoFactorAuth()
key_manager = KeyManager()
blockchain_analyzer = BlockchainAnalyzer()

# Mock user database (in a real implementation, this would be a database)
users_db = {}


# Helper functions
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get the current user from the JWT token."""
    payload = jwt_handler.decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username = payload["sub"]
    if username not in users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return users_db[username]


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get the current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )
    
    return current_user


# Authentication endpoints
@router.post("/register", response_model=Dict[str, Any])
async def register_user(
    username: str = Body(...),
    email: str = Body(...),
    password: str = Body(...),
    role: UserRole = Body(UserRole.VIEWER)
) -> Dict[str, Any]:
    """Register a new user."""
    if username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    
    # Hash password (in a real implementation, use a proper password hashing library)
    hashed_password = f"hashed_{password}"
    
    # Create user
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        role=role
    )
    
    # Store user
    users_db[username] = user
    
    return {
        "username": username,
        "email": email,
        "role": role,
        "message": "User registered successfully"
    }


@router.post("/token", response_model=Dict[str, Any])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Dict[str, Any]:
    """Login to get an access token."""
    username = form_data.username
    password = form_data.password
    
    if username not in users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = users_db[username]
    
    # Verify password (in a real implementation, use a proper password verification)
    if user.hashed_password != f"hashed_{password}":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if 2FA is enabled
    if user.two_factor_enabled:
        return {
            "requires_2fa": True,
            "username": username,
            "message": "Two-factor authentication required"
        }
    
    # Create tokens
    access_token = jwt_handler.create_access_token({"sub": username})
    refresh_token = jwt_handler.create_refresh_token({"sub": username})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/token/2fa", response_model=Dict[str, Any])
async def verify_2fa_token(
    username: str = Body(...),
    totp_token: str = Body(...)
) -> Dict[str, Any]:
    """Verify 2FA token and get an access token."""
    if username not in users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = users_db[username]
    
    if not user.two_factor_enabled or not user.two_factor_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Two-factor authentication not enabled",
        )
    
    # Verify TOTP token
    if not two_factor_auth.verify_totp(user.two_factor_secret, totp_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid two-factor token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create tokens
    access_token = jwt_handler.create_access_token({"sub": username})
    refresh_token = jwt_handler.create_refresh_token({"sub": username})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/token/refresh", response_model=Dict[str, Any])
async def refresh_token(
    refresh_token: str = Body(...)
) -> Dict[str, Any]:
    """Refresh an access token."""
    new_access_token = jwt_handler.refresh_access_token(refresh_token)
    
    if not new_access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


# Two-factor authentication endpoints
@router.post("/2fa/enable", response_model=Dict[str, Any])
async def enable_2fa(
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Enable two-factor authentication for a user."""
    if current_user.two_factor_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Two-factor authentication already enabled",
        )
    
    # Generate secret
    secret = two_factor_auth.generate_secret()
    
    # Generate backup codes
    backup_key, backup_codes = two_factor_auth.generate_backup_codes()
    
    # Update user
    current_user.two_factor_secret = secret
    current_user.backup_codes = backup_codes
    
    # Get provisioning URI for QR code
    provisioning_uri = two_factor_auth.get_provisioning_uri(current_user.username, secret)
    
    return {
        "secret": secret,
        "provisioning_uri": provisioning_uri,
        "backup_codes": list(backup_codes.keys()),
        "message": "Two-factor authentication enabled"
    }


@router.post("/2fa/verify", response_model=Dict[str, Any])
async def verify_2fa(
    totp_token: str = Body(...),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Verify two-factor authentication setup."""
    if not current_user.two_factor_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Two-factor authentication not set up",
        )
    
    # Verify TOTP token
    if not two_factor_auth.verify_totp(current_user.two_factor_secret, totp_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid two-factor token",
        )
    
    # Enable 2FA
    current_user.two_factor_enabled = True
    
    return {
        "message": "Two-factor authentication verified and enabled"
    }


@router.post("/2fa/disable", response_model=Dict[str, Any])
async def disable_2fa(
    totp_token: str = Body(...),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Disable two-factor authentication for a user."""
    if not current_user.two_factor_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Two-factor authentication not enabled",
        )
    
    # Verify TOTP token
    if not two_factor_auth.verify_totp(current_user.two_factor_secret, totp_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid two-factor token",
        )
    
    # Disable 2FA
    current_user.two_factor_enabled = False
    current_user.two_factor_secret = None
    current_user.backup_codes = {}
    
    return {
        "message": "Two-factor authentication disabled"
    }


# API key management endpoints
@router.post("/api-keys", response_model=Dict[str, Any])
async def store_api_key(
    service: str = Body(...),
    key_id: str = Body(...),
    api_key: str = Body(...),
    api_secret: Optional[str] = Body(None),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Store an API key."""
    # Check permission
    if not current_user.has_permission(Permission.MANAGE_API_KEYS):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Store API key
    success = key_manager.store_api_key(service, key_id, api_key, api_secret)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to store API key",
        )
    
    return {
        "service": service,
        "key_id": key_id,
        "message": "API key stored successfully"
    }


@router.get("/api-keys/{service}/{key_id}", response_model=Dict[str, Any])
async def get_api_key(
    service: str,
    key_id: str,
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Get an API key."""
    # Check permission
    if not current_user.has_permission(Permission.VIEW_API_KEYS):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Get API key
    key_data = key_manager.get_api_key(service, key_id)
    
    if not key_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found",
        )
    
    return {
        "service": service,
        "key_id": key_id,
        "api_key": key_data.get("api_key"),
        "has_secret": "api_secret" in key_data
    }


@router.delete("/api-keys/{service}/{key_id}", response_model=Dict[str, Any])
async def delete_api_key(
    service: str,
    key_id: str,
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Delete an API key."""
    # Check permission
    if not current_user.has_permission(Permission.MANAGE_API_KEYS):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Delete API key
    success = key_manager.delete_api_key(service, key_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found",
        )
    
    return {
        "service": service,
        "key_id": key_id,
        "message": "API key deleted successfully"
    }


# Blockchain compliance endpoints
@router.get("/compliance/address/{blockchain}/{address}", response_model=Dict[str, Any])
async def check_address_risk(
    blockchain: str,
    address: str,
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Check the risk score of a blockchain address."""
    # Check risk score
    risk_data = blockchain_analyzer.check_address_risk(address, blockchain)
    
    return risk_data


@router.get("/compliance/transaction/{blockchain}/{transaction_hash}", response_model=Dict[str, Any])
async def check_transaction_risk(
    blockchain: str,
    transaction_hash: str,
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Check the risk score of a blockchain transaction."""
    # Check risk score
    risk_data = blockchain_analyzer.check_transaction_risk(transaction_hash, blockchain)
    
    return risk_data


@router.get("/compliance/sanctioned/{blockchain}/{address}", response_model=Dict[str, bool])
async def is_address_sanctioned(
    blockchain: str,
    address: str,
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, bool]:
    """Check if an address is on a sanctions list."""
    # Check if sanctioned
    is_sanctioned = blockchain_analyzer.is_address_sanctioned(address, blockchain)
    
    return {
        "is_sanctioned": is_sanctioned
    }
