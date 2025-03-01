"""
Main FastAPI application for QT.AI trading bot.

This module creates the main FastAPI application and includes all API routers.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api import api_router
from app.security.secure_comms import SecureComms

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="QT.AI Trading Bot",
    description="Advanced trading bot with AI/ML capabilities, user setup, and account management",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "https://qt-ai.example.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "QT.AI Trading Bot",
        "version": "0.1.0",
        "status": "running"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy"
    }

# Run the application
if __name__ == "__main__":
    import uvicorn
    
    # Get SSL context if available
    ssl_context = None
    if os.environ.get("USE_HTTPS", "false").lower() == "true":
        cert_file = os.environ.get("SSL_CERT_FILE")
        key_file = os.environ.get("SSL_KEY_FILE")
        
        if cert_file and key_file:
            secure_comms = SecureComms(cert_file=cert_file, key_file=key_file)
            ssl_context = secure_comms.get_ssl_context()
    
    # Run server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        ssl_keyfile=os.environ.get("SSL_KEY_FILE"),
        ssl_certfile=os.environ.get("SSL_CERT_FILE")
    )
