from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from src.database.config import get_db
from src.database.models import Strategy, User, StrategySymbol
from src.schemas.strategy import (
    Strategy as StrategySchema,
    StrategyCreate,
    StrategyUpdate,
    StrategyWithPerformance
)
from src.api.dependencies.auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[StrategySchema])
async def get_strategies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all strategies for the current user.
    """
    strategies = db.query(Strategy).filter(
        Strategy.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return strategies

@router.post("/", response_model=StrategySchema)
async def create_strategy(
    strategy: StrategyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new strategy.
    """
    db_strategy = Strategy(
        user_id=current_user.id,
        name=strategy.name,
        description=strategy.description,
        strategy_type=strategy.strategy_type.value,
        asset_class=strategy.asset_class,
        parameters=strategy.parameters,
        is_active=strategy.is_active
    )
    
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    
    return db_strategy

@router.get("/{strategy_id}", response_model=StrategySchema)
async def get_strategy(
    strategy_id: int = Path(..., description="The ID of the strategy to get"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific strategy by ID.
    """
    strategy = db.query(Strategy).filter(
        Strategy.id == strategy_id,
        Strategy.user_id == current_user.id
    ).first()
    
    if not strategy:
        raise HTTPException(
            status_code=404,
            detail="Strategy not found"
        )
    
    return strategy

@router.put("/{strategy_id}", response_model=StrategySchema)
async def update_strategy(
    strategy_id: int,
    strategy_update: StrategyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a strategy.
    """
    db_strategy = db.query(Strategy).filter(
        Strategy.id == strategy_id,
        Strategy.user_id == current_user.id
    ).first()
    
    if not db_strategy:
        raise HTTPException(
            status_code=404,
            detail="Strategy not found"
        )
    
    # Update fields if provided
    update_data = strategy_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_strategy, key, value)
    
    db.commit()
    db.refresh(db_strategy)
    
    return db_strategy

@router.delete("/{strategy_id}", response_model=StrategySchema)
async def delete_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a strategy.
    """
    db_strategy = db.query(Strategy).filter(
        Strategy.id == strategy_id,
        Strategy.user_id == current_user.id
    ).first()
    
    if not db_strategy:
        raise HTTPException(
            status_code=404,
            detail="Strategy not found"
        )
    
    db.delete(db_strategy)
    db.commit()
    
    return db_strategy

@router.post("/{strategy_id}/activate", response_model=StrategySchema)
async def activate_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Activate a strategy.
    """
    db_strategy = db.query(Strategy).filter(
        Strategy.id == strategy_id,
        Strategy.user_id == current_user.id
    ).first()
    
    if not db_strategy:
        raise HTTPException(
            status_code=404,
            detail="Strategy not found"
        )
    
    db_strategy.is_active = True
    db.commit()
    db.refresh(db_strategy)
    
    return db_strategy

@router.post("/{strategy_id}/deactivate", response_model=StrategySchema)
async def deactivate_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Deactivate a strategy.
    """
    db_strategy = db.query(Strategy).filter(
        Strategy.id == strategy_id,
        Strategy.user_id == current_user.id
    ).first()
    
    if not db_strategy:
        raise HTTPException(
            status_code=404,
            detail="Strategy not found"
        )
    
    db_strategy.is_active = False
    db.commit()
    db.refresh(db_strategy)
    
    return db_strategy
