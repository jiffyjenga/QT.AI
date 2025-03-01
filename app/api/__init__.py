"""
API package for QT.AI trading bot.

This module contains all API routers and endpoints.
"""
from fastapi import APIRouter

from app.api.endpoints import users, accounts, setup

# Create main API router
api_router = APIRouter()

# Include endpoint routers
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(setup.router, prefix="/setup", tags=["setup"])
