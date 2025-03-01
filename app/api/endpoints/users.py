from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from app.models.user import User, UserCreate, UserUpdate
from app.security.auth import get_current_user, get_current_active_user
from app.security.password import get_password_hash
from app.db import create_user, get_user, update_user, delete_user, get_user_by_email, get_user_by_username

router = APIRouter()

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_new_user(user_create: UserCreate):
    # Check if user with email already exists
    db_user = get_user_by_email(user_create.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # If username is not provided, generate one from email
    if not user_create.username:
        user_create.username = user_create.email.split('@')[0]
    
    # Check if username already exists
    db_user = get_user_by_username(user_create.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_create.password)
    user_data = user_create.dict(exclude={"password"})
    user_data["hashed_password"] = hashed_password
    
    created_user = create_user(user_data)
    return User(**created_user)

@router.get("/me", response_model=User)
async def read_users_me():
    """
    Get the current user.
    
    Returns:
        Current user
    """
    # Return the default user for single-user mode
    from app.db import db
    
    users = list(db["users"].values())
    if users:
        return users[0]
    
    # If no users exist, return a default user
    return {
        "id": "default_user",
        "email": "auto@qtai.test",
        "username": "auto_user",
        "full_name": "Auto User",
        "role": "user",
        "two_factor_enabled": False,
        "two_factor_method": "none",
        "setup_completed": True,
        "is_active": True
    }

@router.put("/me", response_model=User)
async def update_user_me(user_update: UserUpdate):
    """
    Update the current user.
    
    Args:
        user_update: User update data
        
    Returns:
        Updated user
    """
    # Get the default user for single-user mode
    from app.db import db
    
    users = list(db["users"].values())
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )
    
    current_user = users[0]
    
    # If password is being updated, hash it
    if user_update.password:
        user_update_dict = user_update.dict(exclude={"password"})
        user_update_dict["hashed_password"] = get_password_hash(user_update.password)
    else:
        user_update_dict = user_update.dict(exclude_unset=True)
    
    updated_user = update_user(current_user["id"], user_update_dict)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return User(**updated_user)

@router.get("/{user_id}", response_model=User)
async def read_user(user_id: str):
    """
    Get a user by ID.
    
    Args:
        user_id: User ID
        
    Returns:
        User
    """
    # In single-user mode, always allow access to any user
    user = get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return User(**user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id: str):
    """
    Delete a user by ID.
    
    Args:
        user_id: User ID
        
    Returns:
        None
    """
    # In single-user mode, always allow deletion of any user
    success = delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return None
