"""
Debug login functionality for QT.AI trading bot.

This script tests the login functionality with the demo account credentials.
"""
import os
import sys
import json
import requests
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('debug_login.log')
    ]
)
logger = logging.getLogger(__name__)

def test_login(email, password):
    """Test login with the given credentials."""
    logger.info(f"Testing login with email: {email}")
    
    try:
        # Make login request
        response = requests.post(
            "http://localhost:8000/api/auth/token",
            data={"username": email, "password": password}
        )
        
        # Log response
        logger.info(f"Login response status code: {response.status_code}")
        
        if response.status_code == 200:
            logger.info("Login successful!")
            logger.info(f"Response: {response.json()}")
            return True
        else:
            logger.error(f"Login failed: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return False

def check_user_exists(email):
    """Check if a user with the given email exists."""
    logger.info(f"Checking if user exists: {email}")
    
    # Check if data directory exists
    data_dir = Path("data")
    if not data_dir.exists():
        logger.error("Data directory does not exist")
        return False
    
    # Check if users file exists
    users_file = data_dir / "users.json"
    if not users_file.exists():
        logger.error("Users file does not exist")
        return False
    
    # Load users
    with open(users_file, "r") as f:
        users = json.load(f)
    
    # Check if user exists
    user = next((user for user in users if user.get("email") == email), None)
    if user:
        logger.info(f"User found: {user}")
        return True
    else:
        logger.error(f"User not found: {email}")
        return False

def create_demo_user():
    """Create a demo user for testing."""
    logger.info("Creating demo user")
    
    import hashlib
    import uuid
    import datetime
    
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Create users file if it doesn't exist
    users_file = data_dir / "users.json"
    if not users_file.exists():
        with open(users_file, "w") as f:
            json.dump([], f)
    
    # Load existing users
    with open(users_file, "r") as f:
        users = json.load(f)
    
    # Check if demo user already exists
    demo_email = "demo@qtai.test"
    demo_user = next((user for user in users if user.get("email") == demo_email), None)
    
    if demo_user:
        logger.info(f"Demo user already exists: {demo_email}")
        return
    
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
    
    # Add demo user to users
    users.append(demo_user)
    
    # Save updated users
    with open(users_file, "w") as f:
        json.dump(users, f, indent=2)
    
    logger.info(f"Demo user created: {demo_email}")

def main():
    """Main function."""
    try:
        logger.info("=== Starting Login Debugging ===")
        
        # Create demo user
        create_demo_user()
        
        # Check if demo user exists
        demo_email = "demo@qtai.test"
        demo_password = "demo123"
        
        user_exists = check_user_exists(demo_email)
        logger.info(f"User exists: {user_exists}")
        
        # Test login
        login_successful = test_login(demo_email, demo_password)
        logger.info(f"Login successful: {login_successful}")
        
        logger.info("=== Login Debugging Complete ===")
        
        return 0
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
