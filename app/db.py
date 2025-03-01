"""
Database module for QT.AI trading bot.

This module provides database functionality for the QT.AI trading bot.
"""
import os
import json
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Database file path
DB_FILE = os.environ.get("DB_FILE", "test_db.json")

# In-memory database for development
db = {
    "users": {},
    "accounts": {},
    "transactions": {},
    "api_keys": {},
}

def load_db():
    """Load database from file."""
    global db
    
    try:
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r") as f:
                db = json.load(f)
            logger.debug(f"Loaded database from {DB_FILE}")
        else:
            logger.debug(f"Database file {DB_FILE} not found, using in-memory database")
    except Exception as e:
        logger.error(f"Error loading database: {str(e)}")

def save_db():
    """Save database to file."""
    try:
        with open(DB_FILE, "w") as f:
            json.dump(db, f, indent=2, default=str)
        logger.debug(f"Saved database to {DB_FILE}")
    except Exception as e:
        logger.error(f"Error saving database: {str(e)}")

# Load database on module import
load_db()

# User functions
def create_user(user_data):
    """Create a new user."""
    try:
        user_id = str(uuid.uuid4())
        now = datetime.now()
        
        user = {
            "id": user_id,
            "created_at": now,
            "updated_at": now,
            "is_active": True,
            **user_data
        }
        
        db["users"][user_id] = user
        save_db()
        
        # Create account for user
        create_account({
            "user_id": user_id,
            "balance": 0,
            "allocated_balance": 0,
            "currency": "USD"
        })
        
        return user
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return None

def get_user(user_id):
    """Get a user by ID."""
    return db["users"].get(user_id)

def get_user_by_email(email):
    """Get a user by email."""
    for user in db["users"].values():
        if user["email"] == email:
            return user
    return None

def get_user_by_username(username):
    """Get a user by username."""
    for user in db["users"].values():
        if user.get("username") == username:
            return user
    return None

def update_user(user_id, user_data):
    """Update a user."""
    user = get_user(user_id)
    
    if not user:
        return None
    
    user.update(user_data)
    user["updated_at"] = datetime.now()
    
    db["users"][user_id] = user
    save_db()
    
    return user

def delete_user(user_id):
    """Delete a user."""
    if user_id not in db["users"]:
        return False
    
    del db["users"][user_id]
    save_db()
    
    return True

# Account functions
def create_account(account_data):
    """Create a new account."""
    try:
        account_id = str(uuid.uuid4())
        now = datetime.now()
        
        account = {
            "id": account_id,
            "created_at": now,
            "updated_at": now,
            **account_data
        }
        
        db["accounts"][account_id] = account
        save_db()
        
        return account
    except Exception as e:
        logger.error(f"Error creating account: {str(e)}")
        return None

def get_account(account_id):
    """Get an account by ID."""
    return db["accounts"].get(account_id)

def get_account_by_user_id(user_id):
    """Get an account by user ID."""
    for account in db["accounts"].values():
        if account["user_id"] == user_id:
            return account
    return None

def update_account(account_id, account_data):
    """Update an account."""
    account = get_account(account_id)
    
    if not account:
        return None
    
    account.update(account_data)
    account["updated_at"] = datetime.now()
    
    db["accounts"][account_id] = account
    save_db()
    
    return account

def delete_account(account_id):
    """Delete an account."""
    if account_id not in db["accounts"]:
        return False
    
    del db["accounts"][account_id]
    save_db()
    
    return True

# Transaction functions
def create_transaction(transaction_data):
    """Create a new transaction."""
    try:
        transaction_id = str(uuid.uuid4())
        now = datetime.now()
        
        transaction = {
            "id": transaction_id,
            "created_at": now,
            "updated_at": now,
            **transaction_data
        }
        
        db["transactions"][transaction_id] = transaction
        save_db()
        
        return transaction
    except Exception as e:
        logger.error(f"Error creating transaction: {str(e)}")
        return None

def get_transaction(transaction_id):
    """Get a transaction by ID."""
    return db["transactions"].get(transaction_id)

def get_transactions_by_account_id(account_id):
    """Get transactions by account ID."""
    return [
        transaction
        for transaction in db["transactions"].values()
        if transaction["account_id"] == account_id
    ]

def update_transaction(transaction_id, transaction_data):
    """Update a transaction."""
    transaction = get_transaction(transaction_id)
    
    if not transaction:
        return None
    
    transaction.update(transaction_data)
    transaction["updated_at"] = datetime.now()
    
    db["transactions"][transaction_id] = transaction
    save_db()
    
    return transaction

def delete_transaction(transaction_id):
    """Delete a transaction."""
    if transaction_id not in db["transactions"]:
        return False
    
    del db["transactions"][transaction_id]
    save_db()
    
    return True

# API key functions
def create_api_key(api_key_data):
    """Create a new API key."""
    try:
        api_key_id = str(uuid.uuid4())
        now = datetime.now()
        
        api_key = {
            "id": api_key_id,
            "created_at": now,
            "updated_at": now,
            **api_key_data
        }
        
        db["api_keys"][api_key_id] = api_key
        save_db()
        
        return api_key
    except Exception as e:
        logger.error(f"Error creating API key: {str(e)}")
        return None

def get_api_key(api_key_id):
    """Get an API key by ID."""
    return db["api_keys"].get(api_key_id)

def get_api_keys_by_user_id(user_id):
    """Get API keys by user ID."""
    return [
        api_key
        for api_key in db["api_keys"].values()
        if api_key["user_id"] == user_id
    ]

def update_api_key(api_key_id, api_key_data):
    """Update an API key."""
    api_key = get_api_key(api_key_id)
    
    if not api_key:
        return None
    
    api_key.update(api_key_data)
    api_key["updated_at"] = datetime.now()
    
    if "last_used" in api_key_data and api_key_data["last_used"] == "now":
        api_key["last_used"] = datetime.now()
    
    db["api_keys"][api_key_id] = api_key
    save_db()
    
    return api_key

def delete_api_key(api_key_id):
    """Delete an API key."""
    if api_key_id not in db["api_keys"]:
        return False
    
    del db["api_keys"][api_key_id]
    save_db()
    
    return True

# Initialize test data if database is empty
if not db["users"]:
    # Create test user
    test_user = create_user({
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "test123"
        "role": "user",
        "two_factor_enabled": False,
        "two_factor_method": "none",
        "setup_completed": True
    })
    
    # Create test account
    test_account = get_account_by_user_id(test_user["id"])
    update_account(test_account["id"], {
        "balance": 10000,
        "allocated_balance": 5000,
        "currency": "USD"
    })
    
    logger.info(f"Loaded test database with {len(db['users'])} users, {len(db['accounts'])} accounts, {len(db['transactions'])} transactions, and {len(db['api_keys'])} API keys")
