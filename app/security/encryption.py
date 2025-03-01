"""
Encryption module for QT.AI trading bot.

This module provides encryption functionality for the QT.AI trading bot.
"""
import os
import base64
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Encryption:
    """Encryption class for QT.AI trading bot."""
    
    _instance = None
    
    def __new__(cls):
        """Create a new instance of Encryption."""
        if cls._instance is None:
            cls._instance = super(Encryption, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize Encryption."""
        if self._initialized:
            return
        
        self._initialized = True
        self.fernet = None
        self.initialize()
    
    def initialize(self):
        """Initialize encryption."""
        try:
            # Get encryption key from environment variable
            encryption_key = os.environ.get("ENCRYPTION_KEY")
            
            if not encryption_key:
                # Generate a new encryption key
                logger.warning("No encryption key found, generating a new one")
                encryption_key = Fernet.generate_key().decode()
                os.environ["ENCRYPTION_KEY"] = encryption_key
            
            # Create Fernet instance
            self.fernet = Fernet(encryption_key.encode())
            logger.debug("Encryption initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing encryption: {str(e)}")
            raise
    
    def encrypt(self, data):
        """
        Encrypt data.
        
        Args:
            data: Data to encrypt
            
        Returns:
            Encrypted data
        """
        if not self.fernet:
            self.initialize()
        
        try:
            if isinstance(data, str):
                data = data.encode()
            
            encrypted_data = self.fernet.encrypt(data)
            return encrypted_data.decode()
        except Exception as e:
            logger.error(f"Error encrypting data: {str(e)}")
            raise
    
    def decrypt(self, data):
        """
        Decrypt data.
        
        Args:
            data: Data to decrypt
            
        Returns:
            Decrypted data
        """
        if not self.fernet:
            self.initialize()
        
        try:
            if isinstance(data, str):
                data = data.encode()
            
            decrypted_data = self.fernet.decrypt(data)
            return decrypted_data.decode()
        except Exception as e:
            logger.error(f"Error decrypting data: {str(e)}")
            raise
    
    def mask_api_key(self, api_key):
        """
        Mask API key.
        
        Args:
            api_key: API key to mask
            
        Returns:
            Masked API key
        """
        try:
            if len(api_key) <= 8:
                return "*" * len(api_key)
            
            return api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]
        except Exception as e:
            logger.error(f"Error masking API key: {str(e)}")
            raise
    
    @staticmethod
    def generate_key_from_password(password, salt=None):
        """
        Generate encryption key from password.
        
        Args:
            password: Password to generate key from
            salt: Salt to use for key generation
            
        Returns:
            Generated key
        """
        try:
            if not salt:
                salt = os.urandom(16)
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            return key, salt
        except Exception as e:
            logger.error(f"Error generating key from password: {str(e)}")
            raise
