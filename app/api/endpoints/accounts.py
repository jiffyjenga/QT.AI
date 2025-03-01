from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from decimal import Decimal

from app.models.user import User
from app.models.account import Account, AccountCreate, AccountUpdate, AccountTransaction
from app.security.auth import get_current_active_user
from app.db import create_account, get_account, get_account_by_user_id, update_account, add_transaction, delete_account

router = APIRouter()

@router.post("/", response_model=Account, status_code=status.HTTP_201_CREATED)
async def create_new_account(account_create: AccountCreate, current_user: User = Depends(get_current_active_user)):
    # Check if user already has an account
    existing_account = get_account_by_user_id(current_user.id)
    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has an account"
        )
    
    # Create account with initial deposit
    account_data = account_create.dict()
    account_data["user_id"] = current_user.id
    
    # Set initial balances based on initial deposit
    initial_deposit = account_data.pop("initial_deposit", Decimal("0.00"))
    account_data["total_balance"] = initial_deposit
    account_data["available_balance"] = initial_deposit
    account_data["allocated_balance"] = Decimal("0.00")
    
    created_account = create_account(account_data)
    
    # Add initial deposit transaction if amount > 0
    if initial_deposit > Decimal("0.00"):
        transaction = {
            "account_id": created_account["id"],
            "amount": initial_deposit,
            "transaction_type": "deposit",
            "status": "completed",
            "notes": "Initial deposit"
        }
        add_transaction(created_account["id"], transaction)
    
    return Account(**created_account)

@router.get("/me", response_model=Account)
async def read_my_account(current_user: User = Depends(get_current_active_user)):
    account = get_account_by_user_id(current_user.id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    return Account(**account)

@router.put("/me", response_model=Account)
async def update_my_account(account_update: AccountUpdate, current_user: User = Depends(get_current_active_user)):
    # Get current account
    account = get_account_by_user_id(current_user.id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    # Update account
    account_update_dict = account_update.dict(exclude_unset=True)
    updated_account = update_account(account["id"], account_update_dict)
    
    return Account(**updated_account)

@router.post("/me/deposit", response_model=Account)
async def deposit_funds(amount: Decimal, current_user: User = Depends(get_current_active_user)):
    if amount <= Decimal("0.00"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Deposit amount must be greater than zero"
        )
    
    # Get current account
    account = get_account_by_user_id(current_user.id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    # Update balances
    new_total = account["total_balance"] + amount
    new_available = account["available_balance"] + amount
    
    update_data = {
        "total_balance": new_total,
        "available_balance": new_available
    }
    
    updated_account = update_account(account["id"], update_data)
    
    # Add transaction
    transaction = {
        "account_id": account["id"],
        "amount": amount,
        "transaction_type": "deposit",
        "status": "completed",
        "notes": "User deposit"
    }
    add_transaction(account["id"], transaction)
    
    return Account(**updated_account)

@router.post("/me/withdraw", response_model=Account)
async def withdraw_funds(amount: Decimal, current_user: User = Depends(get_current_active_user)):
    if amount <= Decimal("0.00"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Withdrawal amount must be greater than zero"
        )
    
    # Get current account
    account = get_account_by_user_id(current_user.id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    # Check if sufficient funds
    if account["available_balance"] < amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient available balance"
        )
    
    # Update balances
    new_total = account["total_balance"] - amount
    new_available = account["available_balance"] - amount
    
    update_data = {
        "total_balance": new_total,
        "available_balance": new_available
    }
    
    updated_account = update_account(account["id"], update_data)
    
    # Add transaction
    transaction = {
        "account_id": account["id"],
        "amount": amount,
        "transaction_type": "withdrawal",
        "status": "completed",
        "notes": "User withdrawal"
    }
    add_transaction(account["id"], transaction)
    
    return Account(**updated_account)

@router.post("/me/allocate", response_model=Account)
async def allocate_trading_funds(amount: Decimal, asset_type: str, asset_id: Optional[str] = None, current_user: User = Depends(get_current_active_user)):
    if amount <= Decimal("0.00"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Allocation amount must be greater than zero"
        )
    
    # Get current account
    account = get_account_by_user_id(current_user.id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    # Check if sufficient funds
    if account["available_balance"] < amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient available balance"
        )
    
    # Update balances
    new_available = account["available_balance"] - amount
    new_allocated = account["allocated_balance"] + amount
    
    update_data = {
        "available_balance": new_available,
        "allocated_balance": new_allocated
    }
    
    updated_account = update_account(account["id"], update_data)
    
    # Add transaction
    transaction = {
        "account_id": account["id"],
        "amount": amount,
        "transaction_type": "allocation",
        "asset_type": asset_type,
        "asset_id": asset_id,
        "status": "completed",
        "notes": f"Allocated for trading {asset_type}"
    }
    add_transaction(account["id"], transaction)
    
    return Account(**updated_account)

@router.post("/me/deallocate", response_model=Account)
async def deallocate_trading_funds(amount: Decimal, asset_type: str, asset_id: Optional[str] = None, current_user: User = Depends(get_current_active_user)):
    if amount <= Decimal("0.00"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Deallocation amount must be greater than zero"
        )
    
    # Get current account
    account = get_account_by_user_id(current_user.id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    # Check if sufficient allocated funds
    if account["allocated_balance"] < amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient allocated balance"
        )
    
    # Update balances
    new_available = account["available_balance"] + amount
    new_allocated = account["allocated_balance"] - amount
    
    update_data = {
        "available_balance": new_available,
        "allocated_balance": new_allocated
    }
    
    updated_account = update_account(account["id"], update_data)
    
    # Add transaction
    transaction = {
        "account_id": account["id"],
        "amount": amount,
        "transaction_type": "deallocation",
        "asset_type": asset_type,
        "asset_id": asset_id,
        "status": "completed",
        "notes": f"Deallocated from trading {asset_type}"
    }
    add_transaction(account["id"], transaction)
    
    return Account(**updated_account)

@router.get("/{account_id}", response_model=Account)
async def read_account(account_id: str, current_user: User = Depends(get_current_active_user)):
    # Only admins can view other accounts
    account = get_account(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    # Check permissions
    if current_user.role != "admin" and account["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return Account(**account)
