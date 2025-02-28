"""
API module for QT.AI trading bot.

This module provides API endpoints for the trading bot, including
authentication, market data, trading, and security features.
"""
from fastapi import APIRouter

from app.api.security.router import router as security_router

# Create main API router
api_router = APIRouter()

# Include security router
api_router.include_router(security_router)

# Include other routers here
# api_router.include_router(market_router)
# api_router.include_router(trading_router)
# api_router.include_router(strategy_router)
# api_router.include_router(user_router)
