"""
API key management endpoints for QT.AI trading bot.

This module provides API key management endpoints for the QT.AI trading bot.
"""
import logging
import traceback
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.api_key import ApiKey, ApiKeyCreate, ApiKeyUpdate
from app.models.user import User
from app.security.auth import get_current_active_user
from app.security.encryption import Encryption
from app.db import create_api_key, get_api_key, get_api_keys_by_user_id, update_api_key, delete_api_key, get_account_by_user_id

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize encryption
encryption = Encryption()

@router.post("/", response_model=ApiKey, status_code=status.HTTP_201_CREATED)
async def create_new_api_key(api_key_create: ApiKeyCreate, current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """
    Create a new API key.
    
    Args:
        api_key_create: API key data
        current_user: Current user
        
    Returns:
        Created API key
    """
    try:
        logger.debug(f"Creating new API key for user {current_user['id']}")
        
        # Get user account
        account = get_account_by_user_id(current_user["id"])
        if not account:
            logger.error(f"Account not found for user {current_user['id']}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        # Encrypt API key and secret
        try:
            encrypted_key = encryption.encrypt(api_key_create.api_key)
            encrypted_secret = encryption.encrypt(api_key_create.api_secret)
            
            # Create masked key for display
            masked_key = encryption.mask_api_key(api_key_create.api_key)
            
            logger.debug(f"Successfully encrypted API key and secret")
        except Exception as e:
            logger.error(f"Error encrypting API key: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error encrypting API key: {str(e)}"
            )
        
        # Create API key
        try:
            api_key_data = {
                "user_id": current_user["id"],
                "exchange": api_key_create.exchange,
                "label": api_key_create.label or f"{api_key_create.exchange.capitalize()} API Key",
                "permissions": api_key_create.permissions or "read",
                "encrypted_key": encrypted_key,
                "encrypted_secret": encrypted_secret,
                "masked_key": masked_key,
                "is_active": True,
                "last_used": None
            }
            
            logger.debug(f"Creating API key with data: {api_key_data}")
            created_api_key = create_api_key(api_key_data)
            
            if not created_api_key:
                logger.error("Failed to create API key in database")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create API key"
                )
            
            logger.debug(f"Successfully created API key: {created_api_key['id']}")
        except Exception as e:
            logger.error(f"Error creating API key in database: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating API key in database: {str(e)}"
            )
        
        # Convert to response model
        try:
            response = ApiKey(
                id=created_api_key["id"],
                user_id=created_api_key["user_id"],
                exchange=created_api_key["exchange"],
                label=created_api_key["label"],
                permissions=created_api_key["permissions"],
                masked_key=created_api_key["masked_key"],
                created_at=created_api_key["created_at"],
                updated_at=created_api_key["updated_at"],
                last_used=created_api_key.get("last_used"),
                is_active=created_api_key["is_active"]
            )
            
            logger.debug(f"Successfully created response model")
            return response
        except Exception as e:
            logger.error(f"Error creating response model: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating response model: {str(e)}"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating API key: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error creating API key: {str(e)}"
        )

@router.get("/", response_model=List[ApiKey])
async def get_api_keys(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """
    Get all API keys for the current user.
    
    Args:
        current_user: Current user
        
    Returns:
        List of API keys
    """
    try:
        logger.debug(f"Getting API keys for user {current_user['id']}")
        
        # Get API keys
        api_keys = get_api_keys_by_user_id(current_user["id"])
        
        # Convert to response model
        return [
            ApiKey(
                id=api_key["id"],
                user_id=api_key["user_id"],
                exchange=api_key["exchange"],
                label=api_key["label"],
                permissions=api_key["permissions"],
                masked_key=api_key["masked_key"],
                created_at=api_key["created_at"],
                updated_at=api_key["updated_at"],
                last_used=api_key.get("last_used"),
                is_active=api_key["is_active"]
            )
            for api_key in api_keys
        ]
    except Exception as e:
        logger.error(f"Error getting API keys: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting API keys: {str(e)}"
        )

@router.get("/{api_key_id}", response_model=ApiKey)
async def get_api_key_by_id(api_key_id: str, current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """
    Get an API key by ID.
    
    Args:
        api_key_id: API key ID
        current_user: Current user
        
    Returns:
        API key
    """
    try:
        logger.debug(f"Getting API key {api_key_id} for user {current_user['id']}")
        
        # Get API key
        api_key = get_api_key(api_key_id)
        
        if not api_key:
            logger.error(f"API key {api_key_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API key not found"
            )
        
        # Check if API key belongs to user
        if api_key["user_id"] != current_user["id"]:
            logger.error(f"API key {api_key_id} does not belong to user {current_user['id']}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this API key"
            )
        
        # Convert to response model
        return ApiKey(
            id=api_key["id"],
            user_id=api_key["user_id"],
            exchange=api_key["exchange"],
            label=api_key["label"],
            permissions=api_key["permissions"],
            masked_key=api_key["masked_key"],
            created_at=api_key["created_at"],
            updated_at=api_key["updated_at"],
            last_used=api_key.get("last_used"),
            is_active=api_key["is_active"]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting API key: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting API key: {str(e)}"
        )

@router.put("/{api_key_id}", response_model=ApiKey)
async def update_api_key_by_id(api_key_id: str, api_key_update: ApiKeyUpdate, current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """
    Update an API key.
    
    Args:
        api_key_id: API key ID
        api_key_update: API key update data
        current_user: Current user
        
    Returns:
        Updated API key
    """
    try:
        logger.debug(f"Updating API key {api_key_id} for user {current_user['id']}")
        
        # Get API key
        api_key = get_api_key(api_key_id)
        
        if not api_key:
            logger.error(f"API key {api_key_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API key not found"
            )
        
        # Check if API key belongs to user
        if api_key["user_id"] != current_user["id"]:
            logger.error(f"API key {api_key_id} does not belong to user {current_user['id']}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this API key"
            )
        
        # Update API key
        update_data = api_key_update.dict(exclude_unset=True)
        updated_api_key = update_api_key(api_key_id, update_data)
        
        if not updated_api_key:
            logger.error(f"Failed to update API key {api_key_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update API key"
            )
        
        # Convert to response model
        return ApiKey(
            id=updated_api_key["id"],
            user_id=updated_api_key["user_id"],
            exchange=updated_api_key["exchange"],
            label=updated_api_key["label"],
            permissions=updated_api_key["permissions"],
            masked_key=updated_api_key["masked_key"],
            created_at=updated_api_key["created_at"],
            updated_at=updated_api_key["updated_at"],
            last_used=updated_api_key.get("last_used"),
            is_active=updated_api_key["is_active"]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating API key: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating API key: {str(e)}"
        )

@router.delete("/{api_key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key_by_id(api_key_id: str, current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """
    Delete an API key.
    
    Args:
        api_key_id: API key ID
        current_user: Current user
    """
    try:
        logger.debug(f"Deleting API key {api_key_id} for user {current_user['id']}")
        
        # Get API key
        api_key = get_api_key(api_key_id)
        
        if not api_key:
            logger.error(f"API key {api_key_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API key not found"
            )
        
        # Check if API key belongs to user
        if api_key["user_id"] != current_user["id"]:
            logger.error(f"API key {api_key_id} does not belong to user {current_user['id']}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this API key"
            )
        
        # Delete API key
        success = delete_api_key(api_key_id)
        
        if not success:
            logger.error(f"Failed to delete API key {api_key_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete API key"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting API key: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting API key: {str(e)}"
        )

@router.post("/{api_key_id}/test", response_model=Dict[str, Any])
async def test_api_key_by_id(api_key_id: str, current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """
    Test an API key.
    
    Args:
        api_key_id: API key ID
        current_user: Current user
        
    Returns:
        Test result
    """
    try:
        logger.debug(f"Testing API key {api_key_id} for user {current_user['id']}")
        
        # Get API key
        api_key = get_api_key(api_key_id)
        
        if not api_key:
            logger.error(f"API key {api_key_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API key not found"
            )
        
        # Check if API key belongs to user
        if api_key["user_id"] != current_user["id"]:
            logger.error(f"API key {api_key_id} does not belong to user {current_user['id']}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to test this API key"
            )
        
        # Decrypt API key and secret
        try:
            decrypted_key = encryption.decrypt(api_key["encrypted_key"])
            decrypted_secret = encryption.decrypt(api_key["encrypted_secret"])
            
            logger.debug(f"Successfully decrypted API key and secret")
        except Exception as e:
            logger.error(f"Error decrypting API key: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error decrypting API key: {str(e)}"
            )
        
        # Test API key (mock implementation for now)
        # In a real implementation, this would connect to the exchange API
        # and verify that the API key and secret are valid
        
        # Update last used timestamp
        update_api_key(api_key_id, {"last_used": "now"})
        
        # Return test result
        return {
            "success": True,
            "message": "API key test successful",
            "exchange": api_key["exchange"],
            "permissions": api_key["permissions"]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error testing API key: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error testing API key: {str(e)}"
        )
