import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import local modules
from api.routers import auth, users, strategies, trades, market, settings
from database.session import engine, SessionLocal
from database import models
from utils.websocket_manager import ConnectionManager
from utils.security import create_access_token, get_current_user

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="QT.AI Trading Bot API",
    description="API for the QT.AI multi-asset trading bot with AI capabilities",
    version="0.1.0",
)

# Configure CORS
origins = [
    "http://localhost:5173",  # Frontend dev server
    "http://localhost:4173",  # Frontend preview server
    "https://qtai.example.com",  # Production frontend (replace with actual domain)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize WebSocket connection manager
ws_manager = ConnectionManager()

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(strategies.router, prefix="/api/strategies", tags=["Strategies"])
app.include_router(trades.router, prefix="/api/trades", tags=["Trades"])
app.include_router(market.router, prefix="/api/market", tags=["Market Data"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to QT.AI Trading Bot API",
        "docs": "/docs",
        "version": "0.1.0",
    }

# WebSocket endpoint for market data
@app.websocket("/ws/market")
async def websocket_market_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket, "market")
    try:
        while True:
            # Wait for any message from client (can be used for subscription management)
            data = await websocket.receive_text()
            # Process the message if needed
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, "market")

# WebSocket endpoint for trade notifications
@app.websocket("/ws/trades")
async def websocket_trades_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket, "trades")
    try:
        while True:
            # Wait for any message from client
            data = await websocket.receive_text()
            # Process the message if needed
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, "trades")

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true",
    )
