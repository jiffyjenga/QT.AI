"""
Key Manager for secure API key storage.

This module provides a simple key manager for testing.
"""
import logging
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

logger = logging.getLogger(__name__)

class KeyManager:
    """Simple key manager for secure API key storage."""
    
    def __init__(self, master_password, salt=None):
        """Initialize the key manager."""
        self.salt = salt or b'salt_'
        self.master_password = master_password.encode()
        self.key = self._derive_key()
        self.cipher = Fernet(self.key)
        logger.info("Initialized key manager")
        
    def _derive_key(self):
        """Derive a key from the master password."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_password))
        return key
    
    def encrypt_api_key(self, api_key):
        """Encrypt an API key."""
        logger.info("Encrypting API key")
        return self.cipher.encrypt(api_key.encode()).decode()
    
    def decrypt_api_key(self, encrypted_api_key):
        """Decrypt an API key."""
        logger.info("Decrypting API key")
        return self.cipher.decrypt(encrypted_api_key.encode()).decode()
