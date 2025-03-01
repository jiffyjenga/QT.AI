from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from decimal import Decimal

from app.models.user import User
from app.models.account import Account, AccountCreate, AccountUpdate, AccountTransaction
from app.security.auth import get_current_active_user
from app.db import create_account, get_account, get_account_by_user_id, update_account, add_transaction, delete_account

router = APIRouter()

@router.post("/", response_model=Account, status_code=status.HTTP_201_CREATED)
async def create_new_account(account_create: AccountCreate):
    """
    Create a new account.
    
    Args:
        account_create: Account creation data
        
    Returns:
        Created account
    """
    # Get the default user for single-user mode
    from app.db import db
    
    users = list(db["users"].values())
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )
    
    user_id = users[0]["id"]
    
    # Check if user already has an account
    existing_account = get_account_by_user_id(user_id)
    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has an account"
        )
    
    # Create account with initial deposit
    account_data = account_create.dict()
    account_data["user_id"] = user_id
    
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
async def read_my_account():
    """
    Get the current user's account.
    
    Returns:
        Account
    """
    # Get the default user for single-user mode
    from app.db import db
    
    users = list(db["users"].values())
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )
    
    user_id = users[0]["id"]
    
    # Get account by user ID
    account = get_account_by_user_id(user_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    return Account(**account)

@router.put("/me", response_model=Account)
async def update_my_account(account_update: AccountUpdate):
    """
    Update the current user's account.
    
    Args:
        account_update: Account update data
        
    Returns:
        Updated account
    """
    # Get the default user for single-user mode
    from app.db import db
    
    users = list(db["users"].values())
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )
    
    user_id = users[0]["id"]
    
    # Get account by user ID
    account = get_account_by_user_id(user_id)
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
async def deposit_funds(amount: Decimal):
    """
    Deposit funds to the current user's account.
    
    Args:
        amount: Deposit amount
        
    Returns:
        Updated account
    """
    if amount <= Decimal("0.00"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Deposit amount must be greater than zero"
        )
    
    # Get the default user for single-user mode
    from app.db import db
    
    users = list(db["users"].values())
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )
    
    user_id = users[0]["id"]
    
    # Get account by user ID
    account = get_account_by_user_id(user_id)
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
async def withdraw_funds(amount: Decimal):
    """
    Withdraw funds from the current user's account.
    
    Args:
        amount: Withdrawal amount
        
    Returns:
        Updated account
    """
    if amount <= Decimal("0.00"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Withdrawal amount must be greater than zero"
        )
    
    # Get the default user for single-user mode
    from app.db import db
    
    users = list(db["users"].values())
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )
    
    user_id = users[0]["id"]
    
    # Get account by user ID
    account = get_account_by_user_id(user_id)
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
async def allocate_trading_funds(amount: Decimal, asset_type: str, asset_id: Optional[str] = None):
    """
    Allocate funds for trading.
    
    Args:
        amount: Allocation amount
        asset_type: Asset type
        asset_id: Asset ID
        
    Returns:
        Updated account
    """
    if amount <= Decimal("0.00"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Allocation amount must be greater than zero"
        )
    
    # Get the default user for single-user mode
    from app.db import db
    
    users = list(db["users"].values())
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )
    
    user_id = users[0]["id"]
    
    # Get account by user ID
    account = get_account_by_user_id(user_id)
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
async def deallocate_trading_funds(amount: Decimal, asset_type: str, asset_id: Optional[str] = None):
    """
    Deallocate funds from trading.
    
    Args:
        amount: Deallocation amount
        asset_type: Asset type
        asset_id: Asset ID
        
    Returns:
        Updated account
    """
    if amount <= Decimal("0.00"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Deallocation amount must be greater than zero"
        )
    
    # Get the default user for single-user mode
    from app.db import db
    
    users = list(db["users"].values())
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )
    
    user_id = users[0]["id"]
    
    # Get account by user ID
    account = get_account_by_user_id(user_id)
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
async def read_account(account_id: str):
    """
    Get an account by ID.
    
    Args:
        account_id: Account ID
        
    Returns:
        Account
    """
    # In single-user mode, always allow access to any account
    account = get_account(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    return Account(**account)
