"""
Fix authentication implementation for QT.AI trading bot.

This script fixes the authentication implementation to ensure login works correctly.
"""
import os
import sys
import json
import hashlib
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('fix_auth.log')
    ]
)
logger = logging.getLogger(__name__)

def fix_auth_implementation():
    """Fix the authentication implementation."""
    logger.info("Fixing authentication implementation")
    
    # Fix the auth.py file
    auth_file = Path("app/security/auth.py")
    if not auth_file.exists():
        logger.error("Auth file does not exist")
        return False
    
    # Read the auth file
    with open(auth_file, "r") as f:
        auth_content = f.read()
    
    # Check if the authenticate_user function needs to be fixed
    if "authenticate_user" not in auth_content:
        logger.error("authenticate_user function not found in auth.py")
        return False
    
    # Fix the authenticate_user function
    new_auth_content = """
from datetime import datetime, timedelta
from typing import Optional, Union, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from app.models.user import User
from app.security.password import verify_password
from app.db import get_user_by_email

# JWT configuration
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# OAuth2 password bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

def authenticate_user(email: str, password: str) -> Optional[User]:
    """
    Authenticate a user with email and password.
    
    Args:
        email: User email
        password: User password
    
    Returns:
        User object if authentication is successful, None otherwise
    """
    user = get_user_by_email(email)
    if not user:
        return None
    
    if not verify_password(password, user["hashed_password"]):
        return None
    
    return User(**{k: v for k, v in user.items() if k != "hashed_password"})

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time
    
    Returns:
        JWT access token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get the current user from the JWT token.
    
    Args:
        token: JWT token
    
    Returns:
        User object
    
    Raises:
        HTTPException: If the token is invalid or the user is not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
        
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = get_user_by_email(email)
    
    if user is None:
        raise credentials_exception
    
    return User(**{k: v for k, v in user.items() if k != "hashed_password"})

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current active user.
    
    Args:
        current_user: Current user
    
    Returns:
        Current active user
    
    Raises:
        HTTPException: If the user is inactive
    """
    # Add logic to check if the user is active
    # For now, all users are considered active
    return current_user
"""
    
    # Write the fixed auth file
    with open(auth_file, "w") as f:
        f.write(new_auth_content)
    
    logger.info("Auth implementation fixed")
    
    # Fix the password.py file
    password_file = Path("app/security/password.py")
    if not password_file.exists():
        logger.error("Password file does not exist")
        return False
    
    # Read the password file
    with open(password_file, "r") as f:
        password_content = f.read()
    
    # Check if the verify_password function needs to be fixed
    if "verify_password" not in password_content:
        logger.error("verify_password function not found in password.py")
        return False
    
    # Fix the verify_password function
    new_password_content = """
import hashlib
from typing import Optional

def get_password_hash(password: str) -> str:
    """
    Hash a password using SHA-256.
    
    Args:
        password: Password to hash
    
    Returns:
        Hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    
    Args:
        plain_password: Password to verify
        hashed_password: Hashed password to verify against
    
    Returns:
        True if the password matches the hash, False otherwise
    """
    return get_password_hash(plain_password) == hashed_password
"""
    
    # Write the fixed password file
    with open(password_file, "w") as f:
        f.write(new_password_content)
    
    logger.info("Password implementation fixed")
    
    # Fix the db.py file
    db_file = Path("app/db.py")
    if not db_file.exists():
        logger.error("DB file does not exist")
        return False
    
    # Read the db file
    with open(db_file, "r") as f:
        db_content = f.read()
    
    # Check if the get_user_by_email function needs to be fixed
    if "get_user_by_email" not in db_content:
        logger.error("get_user_by_email function not found in db.py")
        return False
    
    # Fix the get_user_by_email function
    new_db_content = """
import os
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

# Data directory
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Data files
USERS_FILE = DATA_DIR / "users.json"
ACCOUNTS_FILE = DATA_DIR / "accounts.json"
API_KEYS_FILE = DATA_DIR / "api_keys.json"

# Initialize data files
if not USERS_FILE.exists():
    with open(USERS_FILE, "w") as f:
        json.dump([], f)

if not ACCOUNTS_FILE.exists():
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump([], f)

if not API_KEYS_FILE.exists():
    with open(API_KEYS_FILE, "w") as f:
        json.dump([], f)

# User functions
def get_users() -> List[Dict[str, Any]]:
    """
    Get all users.
    
    Returns:
        List of users
    """
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a user by ID.
    
    Args:
        user_id: User ID
    
    Returns:
        User dict if found, None otherwise
    """
    users = get_users()
    return next((user for user in users if user["id"] == user_id), None)

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Get a user by email.
    
    Args:
        email: User email
    
    Returns:
        User dict if found, None otherwise
    """
    users = get_users()
    return next((user for user in users if user["email"] == email), None)

def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """
    Get a user by username.
    
    Args:
        username: Username
    
    Returns:
        User dict if found, None otherwise
    """
    users = get_users()
    return next((user for user in users if user["username"] == username), None)

def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new user.
    
    Args:
        user_data: User data
    
    Returns:
        Created user
    """
    users = get_users()
    
    # Generate ID if not provided
    if "id" not in user_data:
        user_data["id"] = str(uuid.uuid4())
    
    # Add timestamps
    now = datetime.now().isoformat()
    user_data["created_at"] = now
    user_data["updated_at"] = now
    
    # Add user
    users.append(user_data)
    
    # Save users
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)
    
    return user_data

def update_user(user_id: str, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Update a user.
    
    Args:
        user_id: User ID
        user_data: User data
    
    Returns:
        Updated user if found, None otherwise
    """
    users = get_users()
    
    # Find user
    user_index = next((i for i, user in enumerate(users) if user["id"] == user_id), None)
    
    if user_index is None:
        return None
    
    # Update user
    user_data["updated_at"] = datetime.now().isoformat()
    users[user_index].update(user_data)
    
    # Save users
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)
    
    return users[user_index]

def delete_user(user_id: str) -> bool:
    """
    Delete a user.
    
    Args:
        user_id: User ID
    
    Returns:
        True if the user was deleted, False otherwise
    """
    users = get_users()
    
    # Find user
    user_index = next((i for i, user in enumerate(users) if user["id"] == user_id), None)
    
    if user_index is None:
        return False
    
    # Delete user
    del users[user_index]
    
    # Save users
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)
    
    return True

# Account functions
def get_accounts() -> List[Dict[str, Any]]:
    """
    Get all accounts.
    
    Returns:
        List of accounts
    """
    with open(ACCOUNTS_FILE, "r") as f:
        return json.load(f)

def get_account(account_id: str) -> Optional[Dict[str, Any]]:
    """
    Get an account by ID.
    
    Args:
        account_id: Account ID
    
    Returns:
        Account dict if found, None otherwise
    """
    accounts = get_accounts()
    return next((account for account in accounts if account["id"] == account_id), None)

def get_account_by_user_id(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get an account by user ID.
    
    Args:
        user_id: User ID
    
    Returns:
        Account dict if found, None otherwise
    """
    accounts = get_accounts()
    return next((account for account in accounts if account["user_id"] == user_id), None)

def create_account(account_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new account.
    
    Args:
        account_data: Account data
    
    Returns:
        Created account
    """
    accounts = get_accounts()
    
    # Generate ID if not provided
    if "id" not in account_data:
        account_data["id"] = str(uuid.uuid4())
    
    # Add timestamps
    now = datetime.now().isoformat()
    account_data["created_at"] = now
    account_data["updated_at"] = now
    
    # Add account
    accounts.append(account_data)
    
    # Save accounts
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=2)
    
    return account_data

def update_account(account_id: str, account_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Update an account.
    
    Args:
        account_id: Account ID
        account_data: Account data
    
    Returns:
        Updated account if found, None otherwise
    """
    accounts = get_accounts()
    
    # Find account
    account_index = next((i for i, account in enumerate(accounts) if account["id"] == account_id), None)
    
    if account_index is None:
        return None
    
    # Update account
    account_data["updated_at"] = datetime.now().isoformat()
    accounts[account_index].update(account_data)
    
    # Save accounts
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=2)
    
    return accounts[account_index]

def delete_account(account_id: str) -> bool:
    """
    Delete an account.
    
    Args:
        account_id: Account ID
    
    Returns:
        True if the account was deleted, False otherwise
    """
    accounts = get_accounts()
    
    # Find account
    account_index = next((i for i, account in enumerate(accounts) if account["id"] == account_id), None)
    
    if account_index is None:
        return False
    
    # Delete account
    del accounts[account_index]
    
    # Save accounts
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=2)
    
    return True

# API key functions
def get_api_keys() -> List[Dict[str, Any]]:
    """
    Get all API keys.
    
    Returns:
        List of API keys
    """
    with open(API_KEYS_FILE, "r") as f:
        return json.load(f)

def get_api_key(api_key_id: str) -> Optional[Dict[str, Any]]:
    """
    Get an API key by ID.
    
    Args:
        api_key_id: API key ID
    
    Returns:
        API key dict if found, None otherwise
    """
    api_keys = get_api_keys()
    return next((api_key for api_key in api_keys if api_key["id"] == api_key_id), None)

def get_api_keys_by_user_id(user_id: str) -> List[Dict[str, Any]]:
    """
    Get API keys by user ID.
    
    Args:
        user_id: User ID
    
    Returns:
        List of API keys
    """
    api_keys = get_api_keys()
    return [api_key for api_key in api_keys if api_key["user_id"] == user_id]

def create_api_key(api_key_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new API key.
    
    Args:
        api_key_data: API key data
    
    Returns:
        Created API key
    """
    api_keys = get_api_keys()
    
    # Generate ID if not provided
    if "id" not in api_key_data:
        api_key_data["id"] = str(uuid.uuid4())
    
    # Add timestamps
    now = datetime.now().isoformat()
    api_key_data["created_at"] = now
    api_key_data["updated_at"] = now
    
    # Add API key
    api_keys.append(api_key_data)
    
    # Save API keys
    with open(API_KEYS_FILE, "w") as f:
        json.dump(api_keys, f, indent=2)
    
    return api_key_data

def update_api_key(api_key_id: str, api_key_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Update an API key.
    
    Args:
        api_key_id: API key ID
        api_key_data: API key data
    
    Returns:
        Updated API key if found, None otherwise
    """
    api_keys = get_api_keys()
    
    # Find API key
    api_key_index = next((i for i, api_key in enumerate(api_keys) if api_key["id"] == api_key_id), None)
    
    if api_key_index is None:
        return None
    
    # Update API key
    api_key_data["updated_at"] = datetime.now().isoformat()
    api_keys[api_key_index].update(api_key_data)
    
    # Save API keys
    with open(API_KEYS_FILE, "w") as f:
        json.dump(api_keys, f, indent=2)
    
    return api_keys[api_key_index]

def delete_api_key(api_key_id: str) -> bool:
    """
    Delete an API key.
    
    Args:
        api_key_id: API key ID
    
    Returns:
        True if the API key was deleted, False otherwise
    """
    api_keys = get_api_keys()
    
    # Find API key
    api_key_index = next((i for i, api_key in enumerate(api_keys) if api_key["id"] == api_key_id), None)
    
    if api_key_index is None:
        return False
    
    # Delete API key
    del api_keys[api_key_index]
    
    # Save API keys
    with open(API_KEYS_FILE, "w") as f:
        json.dump(api_keys, f, indent=2)
    
    return True
"""
    
    # Write the fixed db file
    with open(db_file, "w") as f:
        f.write(new_db_content)
    
    logger.info("DB implementation fixed")
    
    return True

def main():
    """Main function."""
    try:
        logger.info("=== Starting Auth Fix ===")
        
        # Fix auth implementation
        auth_fixed = fix_auth_implementation()
        logger.info(f"Auth implementation fixed: {auth_fixed}")
        
        logger.info("=== Auth Fix Complete ===")
        
        return 0
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
