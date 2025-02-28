from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.session import get_db
from database.models import RiskSettings, ExchangeApiKey
from utils.security import get_current_active_user
from models.settings import RiskSettingsBase, RiskSettingsUpdate, RiskSettingsResponse, ApiKeyCreate, ApiKeyResponse

router = APIRouter()

# Risk Settings endpoints
@router.get("/risk", response_model=RiskSettingsResponse)
async def get_risk_settings(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Get user's risk settings or create default if not exists
    risk_settings = db.query(RiskSettings).filter(RiskSettings.user_id == current_user.id).first()
    
    if not risk_settings:
        # Create default risk settings
        risk_settings = RiskSettings(
            user_id=current_user.id,
            max_position_size=1000.0,
            max_daily_loss=500.0,
            max_drawdown=10.0,
            stop_loss_percent=5.0,
            take_profit_percent=10.0,
            confirm_trades=True
        )
        db.add(risk_settings)
        db.commit()
        db.refresh(risk_settings)
    
    return risk_settings

@router.put("/risk", response_model=RiskSettingsResponse)
async def update_risk_settings(
    settings: RiskSettingsUpdate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Get user's risk settings
    risk_settings = db.query(RiskSettings).filter(RiskSettings.user_id == current_user.id).first()
    
    if not risk_settings:
        # Create new risk settings if not exists
        risk_settings = RiskSettings(user_id=current_user.id)
        db.add(risk_settings)
    
    # Update fields that are provided
    for field, value in settings.dict(exclude_unset=True).items():
        setattr(risk_settings, field, value)
    
    db.commit()
    db.refresh(risk_settings)
    
    return risk_settings

# API Keys endpoints
@router.get("/api-keys", response_model=List[ApiKeyResponse])
async def get_api_keys(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Get user's API keys
    api_keys = db.query(ExchangeApiKey).filter(ExchangeApiKey.user_id == current_user.id).all()
    return api_keys

@router.post("/api-keys", response_model=ApiKeyResponse)
async def create_api_key(
    api_key: ApiKeyCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if API key for this exchange already exists
    existing_key = db.query(ExchangeApiKey).filter(
        ExchangeApiKey.user_id == current_user.id,
        ExchangeApiKey.exchange == api_key.exchange
    ).first()
    
    if existing_key:
        # Update existing key
        existing_key.api_key = api_key.api_key
        existing_key.api_secret = api_key.api_secret
        db.commit()
        db.refresh(existing_key)
        return existing_key
    
    # Create new API key
    db_api_key = ExchangeApiKey(
        user_id=current_user.id,
        exchange=api_key.exchange,
        api_key=api_key.api_key,
        api_secret=api_key.api_secret
    )
    
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    
    return db_api_key

@router.delete("/api-keys/{key_id}", response_model=dict)
async def delete_api_key(
    key_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Get API key
    api_key = db.query(ExchangeApiKey).filter(
        ExchangeApiKey.id == key_id,
        ExchangeApiKey.user_id == current_user.id
    ).first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    # Delete API key
    db.delete(api_key)
    db.commit()
    
    return {"message": "API key deleted successfully"}
