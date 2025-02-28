from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database.session import get_db
from database.models import Strategy
from utils.security import get_current_active_user
from models.strategy import StrategyCreate, StrategyUpdate, StrategyResponse, StrategyPerformance
from services.strategy_service import StrategyService

router = APIRouter()
strategy_service = StrategyService()

@router.get("/", response_model=List[StrategyResponse])
async def get_strategies(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all strategies for the current user"""
    strategies = db.query(Strategy).filter(Strategy.user_id == current_user.id).all()
    return strategies

@router.post("/", response_model=StrategyResponse)
async def create_strategy(
    strategy: StrategyCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new strategy"""
    db_strategy = Strategy(
        user_id=current_user.id,
        name=strategy.name,
        description=strategy.description,
        type=strategy.type,
        assets=strategy.assets,
        parameters=strategy.parameters,
        is_active=strategy.is_active
    )
    
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    
    return db_strategy

@router.get("/{strategy_id}", response_model=StrategyResponse)
async def get_strategy(
    strategy_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific strategy by ID"""
    strategy = db.query(Strategy).filter(
        Strategy.id == strategy_id,
        Strategy.user_id == current_user.id
    ).first()
    
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    return strategy

@router.put("/{strategy_id}", response_model=StrategyResponse)
async def update_strategy(
    strategy_id: int,
    strategy_update: StrategyUpdate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a strategy"""
    db_strategy = db.query(Strategy).filter(
        Strategy.id == strategy_id,
        Strategy.user_id == current_user.id
    ).first()
    
    if not db_strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    # Update fields that are provided
    for field, value in strategy_update.dict(exclude_unset=True).items():
        setattr(db_strategy, field, value)
    
    db.commit()
    db.refresh(db_strategy)
    
    return db_strategy

@router.delete("/{strategy_id}", response_model=dict)
async def delete_strategy(
    strategy_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a strategy"""
    db_strategy = db.query(Strategy).filter(
        Strategy.id == strategy_id,
        Strategy.user_id == current_user.id
    ).first()
    
    if not db_strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    db.delete(db_strategy)
    db.commit()
    
    return {"message": "Strategy deleted successfully"}

@router.post("/{strategy_id}/toggle", response_model=StrategyResponse)
async def toggle_strategy(
    strategy_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Toggle a strategy active/inactive"""
    db_strategy = db.query(Strategy).filter(
        Strategy.id == strategy_id,
        Strategy.user_id == current_user.id
    ).first()
    
    if not db_strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    # Toggle active status
    db_strategy.is_active = not db_strategy.is_active
    
    db.commit()
    db.refresh(db_strategy)
    
    return db_strategy

@router.get("/{strategy_id}/performance", response_model=StrategyPerformance)
async def get_strategy_performance(
    strategy_id: int,
    timeframe: str = Query("all", description="Timeframe for performance metrics (e.g. day, week, month, all)"),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get performance metrics for a strategy"""
    # Check if strategy exists and belongs to user
    db_strategy = db.query(Strategy).filter(
        Strategy.id == strategy_id,
        Strategy.user_id == current_user.id
    ).first()
    
    if not db_strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    # Get performance metrics from service
    try:
        performance = await strategy_service.get_strategy_performance(strategy_id, timeframe, db)
        return performance
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
