"""
Database module for QT.AI trading bot.

This module provides database utilities for the QT.AI trading bot.
For simplicity, we're using in-memory dictionaries as our database.
In a production environment, this would be replaced with a proper database like PostgreSQL.
"""
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

# In-memory databases
users_db: Dict[str, Dict[str, Any]] = {}
accounts_db: Dict[str, Dict[str, Any]] = {}
api_keys_db: Dict[str, Dict[str, Any]] = {}
setup_progress_db: Dict[str, Dict[str, Any]] = {}
transactions_db: Dict[str, Dict[str, Any]] = {}

# User database functions
def create_user(user_data: dict) -> dict:
    """Create a new user."""
    user_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    user = {
        "id": user_id,
        "created_at": now,
        "updated_at": now,
        **user_data
    }
    
    users_db[user_id] = user
    return user

def get_user(user_id: str) -> Optional[dict]:
    """Get a user by ID."""
    return users_db.get(user_id)

def get_user_by_email(email: str) -> Optional[dict]:
    """Get a user by email."""
    for user in users_db.values():
        if user.get("email") == email:
            return user
    return None

def get_user_by_username(username: str) -> Optional[dict]:
    """Get a user by username."""
    for user in users_db.values():
        if user.get("username") == username:
            return user
    return None

def update_user(user_id: str, user_data: dict) -> Optional[dict]:
    """Update a user."""
    user = users_db.get(user_id)
    if not user:
        return None
    
    user.update(user_data)
    user["updated_at"] = datetime.utcnow()
    
    return user

def delete_user(user_id: str) -> bool:
    """Delete a user."""
    if user_id in users_db:
        del users_db[user_id]
        return True
    return False

# Account database functions
def create_account(account_data: dict) -> dict:
    """Create a new account."""
    account_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    account = {
        "id": account_id,
        "created_at": now,
        "updated_at": now,
        **account_data
    }
    
    accounts_db[account_id] = account
    return account

def get_account(account_id: str) -> Optional[dict]:
    """Get an account by ID."""
    return accounts_db.get(account_id)

def get_account_by_user_id(user_id: str) -> Optional[dict]:
    """Get an account by user ID."""
    for account in accounts_db.values():
        if account.get("user_id") == user_id:
            return account
    return None

def update_account(account_id: str, account_data: dict) -> Optional[dict]:
    """Update an account."""
    account = accounts_db.get(account_id)
    if not account:
        return None
    
    account.update(account_data)
    account["updated_at"] = datetime.utcnow()
    
    return account

def delete_account(account_id: str) -> bool:
    """Delete an account."""
    if account_id in accounts_db:
        del accounts_db[account_id]
        return True
    return False

# Transaction database functions
def add_transaction(transaction_data: dict) -> dict:
    """Add a new transaction."""
    transaction_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    transaction = {
        "id": transaction_id,
        "created_at": now,
        "updated_at": now,
        **transaction_data
    }
    
    transactions_db[transaction_id] = transaction
    return transaction

def get_transaction(transaction_id: str) -> Optional[dict]:
    """Get a transaction by ID."""
    return transactions_db.get(transaction_id)

def get_transactions_by_account_id(account_id: str) -> List[dict]:
    """Get all transactions for an account."""
    return [
        transaction for transaction in transactions_db.values()
        if transaction.get("account_id") == account_id
    ]

def update_transaction(transaction_id: str, transaction_data: dict) -> Optional[dict]:
    """Update a transaction."""
    transaction = transactions_db.get(transaction_id)
    if not transaction:
        return None
    
    transaction.update(transaction_data)
    transaction["updated_at"] = datetime.utcnow()
    
    return transaction

def delete_transaction(transaction_id: str) -> bool:
    """Delete a transaction."""
    if transaction_id in transactions_db:
        del transactions_db[transaction_id]
        return True
    return False

# API Key database functions
def create_api_key(api_key_data: dict) -> dict:
    """Create a new API key."""
    api_key_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    api_key = {
        "id": api_key_id,
        "created_at": now,
        "updated_at": now,
        **api_key_data
    }
    
    api_keys_db[api_key_id] = api_key
    return api_key

def get_api_key(api_key_id: str) -> Optional[dict]:
    """Get an API key by ID."""
    return api_keys_db.get(api_key_id)

def get_api_keys_by_user_id(user_id: str) -> List[dict]:
    """Get all API keys for a user."""
    return [
        api_key for api_key in api_keys_db.values()
        if api_key.get("user_id") == user_id
    ]

def update_api_key(api_key_id: str, api_key_data: dict) -> Optional[dict]:
    """Update an API key."""
    api_key = api_keys_db.get(api_key_id)
    if not api_key:
        return None
    
    api_key.update(api_key_data)
    api_key["updated_at"] = datetime.utcnow()
    
    return api_key

def delete_api_key(api_key_id: str) -> bool:
    """Delete an API key."""
    if api_key_id in api_keys_db:
        del api_keys_db[api_key_id]
        return True
    return False

# Setup progress database functions
def create_setup_progress(user_id: str) -> dict:
    """Create a new setup progress entry."""
    now = datetime.utcnow()
    
    setup_progress = {
        "user_id": user_id,
        "profile_completed": False,
        "security_completed": False,
        "trading_preferences_completed": False,
        "account_funding_completed": False,
        "setup_completed": False,
        "created_at": now,
        "updated_at": now
    }
    
    setup_progress_db[user_id] = setup_progress
    return setup_progress

def get_setup_progress(user_id: str) -> Optional[dict]:
    """Get setup progress for a user."""
    return setup_progress_db.get(user_id)

def update_setup_progress(user_id: str, setup_progress_data: dict) -> Optional[dict]:
    """Update setup progress for a user."""
    setup_progress = setup_progress_db.get(user_id)
    if not setup_progress:
        return None
    
    setup_progress.update(setup_progress_data)
    setup_progress["updated_at"] = datetime.utcnow()
    
    return setup_progress

def delete_setup_progress(user_id: str) -> bool:
    """Delete setup progress for a user."""
    if user_id in setup_progress_db:
        del setup_progress_db[user_id]
        return True
    return False

# Create a test user for development purposes
def create_test_user():
    """Create a test user for development purposes."""
    from app.security.password import get_password_hash
    
    # Check if test user already exists
    test_user = get_user_by_email("test@example.com")
    if test_user:
        return test_user
    
    # Create test user
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "hashed_password": get_password_hash("test123"),
        "role": "admin",
        "two_factor_enabled": False,
        "two_factor_method": "none",
        "setup_completed": True
    }
    
    return create_user(user_data)

# Create test user on module import
create_test_user()
