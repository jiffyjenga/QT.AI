"""
Two-factor authentication module.

This module provides functionality for two-factor authentication
using TOTP (Time-based One-Time Password).
"""
import os
import base64
from typing import Dict, Tuple
import pyotp
import logging

logger = logging.getLogger(__name__)

class TwoFactorAuth:
    """Two-factor authentication using TOTP."""
    
    def __init__(self, issuer_name: str = "QT.AI Trading Bot"):
        """Initialize the two-factor authentication."""
        self.issuer_name = issuer_name
    
    def generate_secret(self) -> str:
        """Generate a new secret key for TOTP."""
        return pyotp.random_base32()
    
    def get_provisioning_uri(self, username: str, secret: str) -> str:
        """Get the provisioning URI for QR code generation."""
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(name=username, issuer_name=self.issuer_name)
    
    def verify_totp(self, secret: str, token: str) -> bool:
        """Verify a TOTP token."""
        totp = pyotp.TOTP(secret)
        return totp.verify(token)
    
    def generate_backup_codes(self, count: int = 10) -> Tuple[str, Dict[str, str]]:
        """Generate backup codes for 2FA recovery."""
        backup_codes = {}
        backup_key = os.urandom(16).hex()
        
        for i in range(count):
            code = os.urandom(5).hex()
            backup_codes[code] = True
        
        return backup_key, backup_codes
    
    def verify_backup_code(self, backup_codes: Dict[str, bool], code: str) -> bool:
        """Verify a backup code."""
        if code in backup_codes and backup_codes[code]:
            # Mark code as used
            backup_codes[code] = False
            return True
        
        return False
