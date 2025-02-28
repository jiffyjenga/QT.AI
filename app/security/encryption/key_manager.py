"""
Key manager for secure storage of API keys and secrets.

This module provides functionality to securely store and retrieve
API keys and secrets using encryption.
"""
import os
import base64
import json
from pathlib import Path
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging

logger = logging.getLogger(__name__)

class KeyManager:
    """Manager for securely storing and retrieving API keys and secrets."""
    
    def __init__(self, master_key_path: Optional[str] = None, salt_path: Optional[str] = None):
        """Initialize the key manager."""
        self.master_key_path = master_key_path or os.environ.get("MASTER_KEY_PATH", "keys/master.key")
        self.salt_path = salt_path or os.environ.get("SALT_PATH", "keys/salt.key")
        self.keys_path = os.environ.get("KEYS_PATH", "keys/encrypted_keys.json")
        self.fernet = None
        
        # Ensure directories exist
        os.makedirs(os.path.dirname(self.master_key_path), exist_ok=True)
        
        # Initialize encryption
        self._initialize_encryption()
    
    def _initialize_encryption(self):
        """Initialize encryption with master key and salt."""
        # Check if master key exists
        if not os.path.exists(self.master_key_path):
            logger.info("Master key not found. Generating new master key.")
            self._generate_master_key()
        
        # Check if salt exists
        if not os.path.exists(self.salt_path):
            logger.info("Salt not found. Generating new salt.")
            self._generate_salt()
        
        # Load master key and salt
        master_key = self._load_master_key()
        salt = self._load_salt()
        
        # Derive key from master key and salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_key))
        
        # Initialize Fernet cipher
        self.fernet = Fernet(key)
    
    def _generate_master_key(self):
        """Generate a new master key."""
        master_key = os.urandom(32)
        with open(self.master_key_path, 'wb') as f:
            f.write(master_key)
        os.chmod(self.master_key_path, 0o600)  # Restrict permissions
    
    def _generate_salt(self):
        """Generate a new salt."""
        salt = os.urandom(16)
        with open(self.salt_path, 'wb') as f:
            f.write(salt)
        os.chmod(self.salt_path, 0o600)  # Restrict permissions
    
    def _load_master_key(self):
        """Load the master key from file."""
        with open(self.master_key_path, 'rb') as f:
            return f.read()
    
    def _load_salt(self):
        """Load the salt from file."""
        with open(self.salt_path, 'rb') as f:
            return f.read()
    
    def encrypt(self, data: str) -> str:
        """Encrypt data using the master key."""
        if not self.fernet:
            self._initialize_encryption()
        
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt data using the master key."""
        if not self.fernet:
            self._initialize_encryption()
        
        return self.fernet.decrypt(encrypted_data.encode()).decode()
    
    def store_api_key(self, service: str, key_id: str, api_key: str, api_secret: Optional[str] = None) -> bool:
        """Store an API key and optional secret securely."""
        try:
            # Load existing keys
            keys = self.load_keys()
            
            # Create service entry if it doesn't exist
            if service not in keys:
                keys[service] = {}
            
            # Encrypt and store key and secret
            keys[service][key_id] = {
                "api_key": self.encrypt(api_key)
            }
            
            if api_secret:
                keys[service][key_id]["api_secret"] = self.encrypt(api_secret)
            
            # Save keys
            self._save_keys(keys)
            
            logger.info(f"Stored API key for {service}/{key_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error storing API key: {str(e)}")
            return False
    
    def get_api_key(self, service: str, key_id: str) -> Dict[str, str]:
        """Retrieve an API key and optional secret."""
        try:
            # Load keys
            keys = self.load_keys()
            
            # Check if key exists
            if service not in keys or key_id not in keys[service]:
                logger.warning(f"API key not found: {service}/{key_id}")
                return {}
            
            # Decrypt and return key and secret
            result = {}
            if "api_key" in keys[service][key_id]:
                result["api_key"] = self.decrypt(keys[service][key_id]["api_key"])
            
            if "api_secret" in keys[service][key_id]:
                result["api_secret"] = self.decrypt(keys[service][key_id]["api_secret"])
            
            return result
        
        except Exception as e:
            logger.error(f"Error retrieving API key: {str(e)}")
            return {}
    
    def delete_api_key(self, service: str, key_id: str) -> bool:
        """Delete an API key."""
        try:
            # Load keys
            keys = self.load_keys()
            
            # Check if key exists
            if service not in keys or key_id not in keys[service]:
                logger.warning(f"API key not found: {service}/{key_id}")
                return False
            
            # Delete key
            del keys[service][key_id]
            
            # Remove service if empty
            if not keys[service]:
                del keys[service]
            
            # Save keys
            self._save_keys(keys)
            
            logger.info(f"Deleted API key: {service}/{key_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting API key: {str(e)}")
            return False
    
    def load_keys(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        """Load all encrypted keys."""
        if not os.path.exists(self.keys_path):
            return {}
        
        try:
            with open(self.keys_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading keys: {str(e)}")
            return {}
    
    def _save_keys(self, keys: Dict[str, Any]):
        """Save encrypted keys to file."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.keys_path), exist_ok=True)
            
            # Save keys
            with open(self.keys_path, 'w') as f:
                json.dump(keys, f, indent=2)
            
            # Restrict permissions
            os.chmod(self.keys_path, 0o600)
        
        except Exception as e:
            logger.error(f"Error saving keys: {str(e)}")
            raise
