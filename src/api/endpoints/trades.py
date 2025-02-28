from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from src.database.config import get_db
from src.database.models import Trade, User, Strategy
from src.schemas.trade import (
    Trade as TradeSchema,
    TradeCreate,
    TradeUpdate,
    TradeFilter
)
from src.api.dependencies.auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[TradeSchema])
async def get_trades(
    exchange_id: Optional[str] = None,
    symbol: Optional[str] = None,
    strategy_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get trades with optional filtering."""
    query = db.query(Trade).filter(Trade.user_id == current_user.id)
    
    # Apply filters
    if exchange_id:
        query = query.filter(Trade.exchange_id == exchange_id)
    if symbol:
        query = query.filter(Trade.symbol == symbol)
    if strategy_id:
        query = query.filter(Trade.strategy_id == strategy_id)
    
    # Order by timestamp and paginate
    trades = query.order_by(Trade.timestamp.desc()).offset(skip).limit(limit).all()
    
    return trades

@router.post("/", response_model=TradeSchema)
async def create_trade(
    trade: TradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new trade record."""
    # Create trade
    db_trade = Trade(
        user_id=current_user.id,
        strategy_id=trade.strategy_id,
        exchange_id=trade.exchange_id,
        symbol=trade.symbol,
        order_id=trade.order_id,
        order_type=trade.order_type,
        side=trade.side,
        quantity=trade.quantity,
        price=trade.price,
        cost=trade.cost,
        fee=trade.fee,
        timestamp=trade.timestamp,
        status=trade.status,
        notes=trade.notes,
        additional_data=trade.additional_data
    )
    
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    
    return db_trade

@router.get("/{trade_id}", response_model=TradeSchema)
async def get_trade(
    trade_id: int = Path(..., description="The ID of the trade to get"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific trade by ID."""
    trade = db.query(Trade).filter(
        Trade.id == trade_id,
        Trade.user_id == current_user.id
    ).first()
    
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    return trade
