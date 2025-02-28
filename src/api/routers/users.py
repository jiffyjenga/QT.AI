from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.session import get_db
from database.models import User
from utils.security import get_current_active_user, get_password_hash
from models.auth import UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user = Depends(get_current_active_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "is_active": current_user.is_active,
        "is_superuser": current_user.is_superuser,
    }

@router.put("/me", response_model=UserResponse)
async def update_user(
    user_data: dict,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Update user data
    if "email" in user_data:
        # Check if email already exists
        existing_email = db.query(User).filter(User.email == user_data["email"]).first()
        if existing_email and existing_email.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        current_user.email = user_data["email"]
    
    if "username" in user_data:
        # Check if username already exists
        existing_username = db.query(User).filter(User.username == user_data["username"]).first()
        if existing_username and existing_username.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )
        current_user.username = user_data["username"]
    
    if "password" in user_data:
        current_user.hashed_password = get_password_hash(user_data["password"])
    
    db.commit()
    db.refresh(current_user)
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "is_active": current_user.is_active,
        "is_superuser": current_user.is_superuser,
    }
