from datetime import datetime
import uuid
from typing import Dict, List, Optional

# In-memory database for development
users_db: Dict[str, dict] = {}
accounts_db: Dict[str, dict] = {}

def generate_id() -> str:
    return str(uuid.uuid4())

# User database functions
def create_user(user_data: dict) -> dict:
    user_id = generate_id()
    timestamp = datetime.utcnow()
    user = {
        "id": user_id,
        "created_at": timestamp,
        "updated_at": timestamp,
        **user_data
    }
    users_db[user_id] = user
    return user

def get_user(user_id: str) -> Optional[dict]:
    return users_db.get(user_id)

def get_user_by_email(email: str) -> Optional[dict]:
    for user in users_db.values():
        if user["email"] == email:
            return user
    return None

def get_user_by_username(username: str) -> Optional[dict]:
    for user in users_db.values():
        if user["username"] == username:
            return user
    return None

def update_user(user_id: str, update_data: dict) -> Optional[dict]:
    if user_id not in users_db:
        return None
    user = users_db[user_id]
    for key, value in update_data.items():
        if value is not None:
            user[key] = value
    user["updated_at"] = datetime.utcnow()
    return user

def delete_user(user_id: str) -> bool:
    if user_id in users_db:
        del users_db[user_id]
        return True
    return False

# Account database functions
def create_account(account_data: dict) -> dict:
    account_id = generate_id()
    timestamp = datetime.utcnow()
    account = {
        "id": account_id,
        "created_at": timestamp,
        "updated_at": timestamp,
        "transactions": [],
        **account_data
    }
    accounts_db[account_id] = account
    return account

def get_account(account_id: str) -> Optional[dict]:
    return accounts_db.get(account_id)

def get_account_by_user_id(user_id: str) -> Optional[dict]:
    for account in accounts_db.values():
        if account["user_id"] == user_id:
            return account
    return None

def update_account(account_id: str, update_data: dict) -> Optional[dict]:
    if account_id not in accounts_db:
        return None
    account = accounts_db[account_id]
    for key, value in update_data.items():
        if value is not None and key != "transactions":
            account[key] = value
    account["updated_at"] = datetime.utcnow()
    return account

def add_transaction(account_id: str, transaction: dict) -> Optional[dict]:
    if account_id not in accounts_db:
        return None
    account = accounts_db[account_id]
    account["transactions"].append(transaction)
    account["updated_at"] = datetime.utcnow()
    return account

def delete_account(account_id: str) -> bool:
    if account_id in accounts_db:
        del accounts_db[account_id]
        return True
    return False
