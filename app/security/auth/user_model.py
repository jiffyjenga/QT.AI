"""
User model with role-based permissions.

This module defines the user model with role-based access control
for multi-user support.
"""
from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class UserRole(str, Enum):
    """User roles for role-based access control."""
    
    ADMIN = "admin"
    TRADER = "trader"
    ANALYST = "analyst"
    VIEWER = "viewer"


class Permission(str, Enum):
    """Permissions for role-based access control."""
    
    # Strategy permissions
    CREATE_STRATEGY = "create_strategy"
    EDIT_STRATEGY = "edit_strategy"
    DELETE_STRATEGY = "delete_strategy"
    VIEW_STRATEGY = "view_strategy"
    
    # Trade permissions
    EXECUTE_TRADE = "execute_trade"
    APPROVE_TRADE = "approve_trade"
    CANCEL_TRADE = "cancel_trade"
    VIEW_TRADE = "view_trade"
    
    # API key permissions
    MANAGE_API_KEYS = "manage_api_keys"
    VIEW_API_KEYS = "view_api_keys"
    
    # User management permissions
    MANAGE_USERS = "manage_users"
    VIEW_USERS = "view_users"
    
    # Settings permissions
    MANAGE_SETTINGS = "manage_settings"
    VIEW_SETTINGS = "view_settings"
    
    # System permissions
    VIEW_LOGS = "view_logs"
    MANAGE_SYSTEM = "manage_system"


# Role to permissions mapping
ROLE_PERMISSIONS = {
    UserRole.ADMIN: [p for p in Permission],  # All permissions
    UserRole.TRADER: [
        Permission.VIEW_STRATEGY, Permission.CREATE_STRATEGY, Permission.EDIT_STRATEGY,
        Permission.EXECUTE_TRADE, Permission.APPROVE_TRADE, Permission.CANCEL_TRADE, Permission.VIEW_TRADE,
        Permission.VIEW_API_KEYS,
        Permission.VIEW_SETTINGS,
        Permission.VIEW_LOGS
    ],
    UserRole.ANALYST: [
        Permission.VIEW_STRATEGY, Permission.CREATE_STRATEGY, Permission.EDIT_STRATEGY,
        Permission.VIEW_TRADE,
        Permission.VIEW_API_KEYS,
        Permission.VIEW_SETTINGS,
        Permission.VIEW_LOGS
    ],
    UserRole.VIEWER: [
        Permission.VIEW_STRATEGY,
        Permission.VIEW_TRADE,
        Permission.VIEW_SETTINGS
    ]
}


class User:
    """User model with role-based permissions."""
    
    def __init__(self, 
                 username: str,
                 email: str,
                 hashed_password: str,
                 role: UserRole = UserRole.VIEWER,
                 is_active: bool = True,
                 is_verified: bool = False,
                 two_factor_enabled: bool = False,
                 two_factor_secret: Optional[str] = None,
                 backup_codes: Optional[Dict[str, bool]] = None,
                 custom_permissions: Optional[List[Permission]] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        """Initialize a user."""
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
        self.is_active = is_active
        self.is_verified = is_verified
        self.two_factor_enabled = two_factor_enabled
        self.two_factor_secret = two_factor_secret
        self.backup_codes = backup_codes or {}
        self.custom_permissions = custom_permissions or []
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if the user has a specific permission."""
        # Check custom permissions first
        if permission in self.custom_permissions:
            return True
        
        # Check role-based permissions
        return permission in ROLE_PERMISSIONS.get(self.role, [])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary."""
        return {
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "two_factor_enabled": self.two_factor_enabled,
            "custom_permissions": self.custom_permissions,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create user from dictionary."""
        return cls(
            username=data["username"],
            email=data["email"],
            hashed_password=data["hashed_password"],
            role=data.get("role", UserRole.VIEWER),
            is_active=data.get("is_active", True),
            is_verified=data.get("is_verified", False),
            two_factor_enabled=data.get("two_factor_enabled", False),
            two_factor_secret=data.get("two_factor_secret"),
            backup_codes=data.get("backup_codes", {}),
            custom_permissions=data.get("custom_permissions", []),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else None,
            updated_at=datetime.fromisoformat(data["updated_at"]) if "updated_at" in data else None
        )
