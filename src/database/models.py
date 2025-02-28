from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, JSON, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .session import Base

# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    strategies = relationship("Strategy", back_populates="user")
    trades = relationship("Trade", back_populates="user")
    api_keys = relationship("ExchangeApiKey", back_populates="user")
    risk_settings = relationship("RiskSettings", back_populates="user", uselist=False)

# Strategy model
class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    type = Column(String, index=True)  # e.g., trend_following, scalping, mean_reversion, ai_lstm, ai_reinforcement
    assets = Column(JSON)  # List of asset pairs this strategy trades
    parameters = Column(JSON)  # Strategy-specific parameters
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    user = relationship("User", back_populates="strategies")
    trades = relationship("Trade", back_populates="strategy")

# Trade model
class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    type = Column(String, index=True)  # BUY or SELL
    amount = Column(Float)
    price = Column(Float)
    value = Column(Float)  # amount * price
    fee = Column(Float)
    status = Column(String, index=True)  # PENDING, COMPLETED, FAILED, CANCELED
    exchange = Column(String, index=True)
    order_id = Column(String, unique=True, index=True, nullable=True)  # Exchange order ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=True)

    # Relationships
    user = relationship("User", back_populates="trades")
    strategy = relationship("Strategy", back_populates="trades")

# Exchange API Key model
class ExchangeApiKey(Base):
    __tablename__ = "exchange_api_keys"

    id = Column(Integer, primary_key=True, index=True)
    exchange = Column(String, index=True)
    api_key = Column(String)
    api_secret = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    user = relationship("User", back_populates="api_keys")

# Risk Settings model
class RiskSettings(Base):
    __tablename__ = "risk_settings"

    id = Column(Integer, primary_key=True, index=True)
    max_position_size = Column(Float, default=1000.0)
    max_daily_loss = Column(Float, default=500.0)
    max_drawdown = Column(Float, default=10.0)  # Percentage
    stop_loss_percent = Column(Float, default=5.0)
    take_profit_percent = Column(Float, default=10.0)
    confirm_trades = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    user = relationship("User", back_populates="risk_settings")
