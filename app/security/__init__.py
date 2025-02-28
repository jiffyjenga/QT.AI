"""
Security module for QT.AI trading bot.

This module provides security features for the trading bot, including
encrypted storage for API keys, multi-user access controls with role-based
permissions, blockchain analysis for fraud detection and compliance, and
secure communications using HTTPS/WebSockets over TLS.
"""
from app.security.encryption.key_manager import KeyManager
from app.security.auth.jwt_handler import JWTHandler
from app.security.auth.two_factor import TwoFactorAuth
from app.security.auth.user_model import User, UserRole, Permission
from app.security.compliance.blockchain_analyzer import BlockchainAnalyzer
from app.security.secure_comms import SecureComms

__all__ = [
    'KeyManager',
    'JWTHandler',
    'TwoFactorAuth',
    'User',
    'UserRole',
    'Permission',
    'BlockchainAnalyzer',
    'SecureComms'
]
