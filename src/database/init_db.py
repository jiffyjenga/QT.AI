import logging
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime

from .config import engine, Base, SessionLocal
from .models import User, Strategy, AssetClass

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_tables():
    """Create all tables in the database."""
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")

def get_password_hash(password: str) -> str:
    """Hash a password for storing."""
    return pwd_context.hash(password)

def create_initial_data(db: Session):
    """Create initial data for testing."""
    logger.info("Creating initial data...")
    
    # Create admin user if it doesn't exist
    admin_user = db.query(User).filter(User.email == "admin@qtai.com").first()
    if not admin_user:
        admin_user = User(
            email="admin@qtai.com",
            username="admin",
            hashed_password=get_password_hash("adminpassword"),
            is_active=True,
            is_superuser=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        logger.info(f"Admin user created with ID: {admin_user.id}")
    
    # Create demo user if it doesn't exist
    demo_user = db.query(User).filter(User.email == "demo@qtai.com").first()
    if not demo_user:
        demo_user = User(
            email="demo@qtai.com",
            username="demo",
            hashed_password=get_password_hash("demopassword"),
            is_active=True,
            is_superuser=False
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)
        logger.info(f"Demo user created with ID: {demo_user.id}")
    
    # Create sample strategies
    strategies = [
        {
            "name": "Bitcoin Trend Following",
            "description": "Simple trend following strategy for Bitcoin",
            "strategy_type": "trend_following",
            "asset_class": AssetClass.CRYPTO,
            "parameters": {
                "fast_period": 10,
                "slow_period": 30,
                "symbol": "BTC/USDT",
                "exchange": "binance"
            }
        },
        {
            "name": "ETH/BTC Arbitrage",
            "description": "Arbitrage between ETH/BTC on different exchanges",
            "strategy_type": "arbitrage",
            "asset_class": AssetClass.CRYPTO,
            "parameters": {
                "min_profit_pct": 0.5,
                "symbol": "ETH/BTC",
                "exchanges": ["binance", "kraken", "coinbase"]
            }
        },
        {
            "name": "Forex Scalping",
            "description": "Short-term scalping strategy for EUR/USD",
            "strategy_type": "scalping",
            "asset_class": AssetClass.FOREX,
            "parameters": {
                "rsi_period": 14,
                "rsi_overbought": 70,
                "rsi_oversold": 30,
                "symbol": "EUR/USD",
                "exchange": "oanda"
            }
        }
    ]
    
    for strategy_data in strategies:
        # Check if strategy already exists
        existing = db.query(Strategy).filter(
            Strategy.name == strategy_data["name"],
            Strategy.user_id == demo_user.id
        ).first()
        
        if not existing:
            strategy = Strategy(
                user_id=demo_user.id,
                name=strategy_data["name"],
                description=strategy_data["description"],
                strategy_type=strategy_data["strategy_type"],
                asset_class=strategy_data["asset_class"],
                parameters=strategy_data["parameters"],
                is_active=False
            )
            db.add(strategy)
            logger.info(f"Added strategy: {strategy_data['name']}")
    
    db.commit()
    logger.info("Initial data created successfully.")

def init_db():
    """Initialize the database with tables and initial data."""
    create_tables()
    
    # Create initial data
    db = SessionLocal()
    try:
        create_initial_data(db)
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
