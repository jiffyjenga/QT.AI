from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database.session import get_db
from database.models import Trade, Strategy
from utils.security import get_current_active_user
from models.trade import TradeCreate, TradeResponse, TradeHistoryParams, TradeHistoryResponse
from services.trade_service import TradeService

router = APIRouter()
trade_service = TradeService()

@router.post("/", response_model=TradeResponse)
async def create_trade(
    trade: TradeCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new trade (manual trade)"""
    # Check if strategy exists and belongs to user if strategy_id is provided
    if trade.strategy_id:
        strategy = db.query(Strategy).filter(
            Strategy.id == trade.strategy_id,
            Strategy.user_id == current_user.id
        ).first()
        
        if not strategy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Strategy not found"
            )
    
    # Calculate value
    value = trade.amount * trade.price
    
    # Create trade
    db_trade = Trade(
        user_id=current_user.id,
        symbol=trade.symbol,
        type=trade.type,
        amount=trade.amount,
        price=trade.price,
        value=value,
        fee=value * 0.001,  # Assume 0.1% fee
        status="COMPLETED",  # For manual trades, assume completed
        exchange=trade.exchange,
        strategy_id=trade.strategy_id
    )
    
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    
    return db_trade

@router.get("/", response_model=TradeHistoryResponse)
async def get_trades(
    limit: int = Query(50, description="Number of trades to return"),
    offset: int = Query(0, description="Offset for pagination"),
    symbol: Optional[str] = Query(None, description="Filter by symbol"),
    strategy_id: Optional[int] = Query(None, description="Filter by strategy ID"),
    type: Optional[str] = Query(None, description="Filter by trade type (BUY/SELL)"),
    status: Optional[str] = Query(None, description="Filter by status"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get trade history with filters and pagination"""
    # Create filter params
    params = TradeHistoryParams(
        limit=limit,
        offset=offset,
        symbol=symbol,
        strategy_id=strategy_id,
        type=type,
        status=status,
        start_date=start_date,
        end_date=end_date
    )
    
    # Get trades from service
    try:
        trades_response = await trade_service.get_trade_history(current_user.id, params, db)
        return trades_response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{trade_id}", response_model=TradeResponse)
async def get_trade(
    trade_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific trade by ID"""
    trade = db.query(Trade).filter(
        Trade.id == trade_id,
        Trade.user_id == current_user.id
    ).first()
    
    if not trade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade not found"
        )
    
    return trade
