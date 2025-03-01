"""
Create a demo account for QT.AI testing.

This script creates a demo account with test credentials for QT.AI testing.
"""
import os
import sys
import json
import uuid
import hashlib
import datetime
from pathlib import Path

# Create data directory if it doesn't exist
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Create users file if it doesn't exist
users_file = data_dir / "users.json"
if not users_file.exists():
    with open(users_file, "w") as f:
        json.dump([], f)

# Create accounts file if it doesn't exist
accounts_file = data_dir / "accounts.json"
if not accounts_file.exists():
    with open(accounts_file, "w") as f:
        json.dump([], f)

# Create api_keys file if it doesn't exist
api_keys_file = data_dir / "api_keys.json"
if not api_keys_file.exists():
    with open(api_keys_file, "w") as f:
        json.dump([], f)

# Load existing users
with open(users_file, "r") as f:
    users = json.load(f)

# Load existing accounts
with open(accounts_file, "r") as f:
    accounts = json.load(f)

# Load existing API keys
with open(api_keys_file, "r") as f:
    api_keys = json.load(f)

# Check if demo account already exists
demo_email = "demo@qtai.test"
demo_user = next((user for user in users if user.get("email") == demo_email), None)

if demo_user:
    print(f"Demo account already exists: {demo_email}")
    print(f"Password: demo123")
    sys.exit(0)

# Create demo user
demo_user_id = str(uuid.uuid4())
demo_password = "demo123"
demo_hashed_password = hashlib.sha256(demo_password.encode()).hexdigest()

demo_user = {
    "id": demo_user_id,
    "email": demo_email,
    "username": "demo_user",
    "full_name": "Demo User",
    "hashed_password": demo_hashed_password,
    "role": "user",
    "two_factor_enabled": False,
    "two_factor_method": "none",
    "setup_completed": True,
    "created_at": datetime.datetime.now().isoformat(),
    "updated_at": datetime.datetime.now().isoformat()
}

# Create demo account
demo_account_id = str(uuid.uuid4())
demo_account = {
    "id": demo_account_id,
    "user_id": demo_user_id,
    "balance": 10000.0,
    "allocated_funds": 5000.0,
    "available_funds": 5000.0,
    "currency": "USD",
    "status": "active",
    "created_at": datetime.datetime.now().isoformat(),
    "updated_at": datetime.datetime.now().isoformat()
}

# Create demo API keys
demo_api_key_id = str(uuid.uuid4())
demo_api_key = {
    "id": demo_api_key_id,
    "user_id": demo_user_id,
    "exchange": "binance",
    "api_key": "demoAPIKey123456789",
    "api_secret": "demoAPISecret123456789",
    "label": "Demo Binance API Key",
    "permissions": "read,trade",
    "is_active": True,
    "created_at": datetime.datetime.now().isoformat(),
    "updated_at": datetime.datetime.now().isoformat()
}

# Add demo user to users
users.append(demo_user)

# Add demo account to accounts
accounts.append(demo_account)

# Add demo API key to API keys
api_keys.append(demo_api_key)

# Save updated users
with open(users_file, "w") as f:
    json.dump(users, f, indent=2)

# Save updated accounts
with open(accounts_file, "w") as f:
    json.dump(accounts, f, indent=2)

# Save updated API keys
with open(api_keys_file, "w") as f:
    json.dump(api_keys, f, indent=2)

print("Demo account created successfully:")
print(f"Email: {demo_email}")
print(f"Password: {demo_password}")
print(f"Account Balance: ${demo_account['balance']}")
print(f"Allocated Funds: ${demo_account['allocated_funds']}")
print(f"Available Funds: ${demo_account['available_funds']}")
print(f"API Key Exchange: {demo_api_key['exchange']}")
print(f"API Key Label: {demo_api_key['label']}")
