from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from app.models.user import User, UserUpdate
from app.models.account import AccountCreate, Account
from app.security.auth import get_current_user
from app.db import update_user, get_user_by_email, get_account_by_user_id
from app.api.endpoints.accounts import create_new_account

router = APIRouter()

class SetupStep(BaseModel):
    step: str
    completed: bool
    data: Optional[Dict[str, Any]] = None

class SetupWizardStatus(BaseModel):
    user_id: str
    completed: bool
    current_step: str
    steps: List[SetupStep]

# Store setup wizard state in memory (would be in database in production)
setup_wizard_state: Dict[str, SetupWizardStatus] = {}

def get_or_create_wizard_state(user_id: str) -> SetupWizardStatus:
    if user_id not in setup_wizard_state:
        setup_wizard_state[user_id] = SetupWizardStatus(
            user_id=user_id,
            completed=False,
            current_step="profile",
            steps=[
                SetupStep(step="profile", completed=False),
                SetupStep(step="security", completed=False),
                SetupStep(step="trading_preferences", completed=False),
                SetupStep(step="account_funding", completed=False),
                SetupStep(step="confirmation", completed=False)
            ]
        )
    return setup_wizard_state[user_id]

@router.get("/status", response_model=SetupWizardStatus)
async def get_setup_status(current_user: User = Depends(get_current_user)):
    # Check if user has completed setup
    if current_user.setup_completed:
        return SetupWizardStatus(
            user_id=current_user.id,
            completed=True,
            current_step="completed",
            steps=[
                SetupStep(step="profile", completed=True),
                SetupStep(step="security", completed=True),
                SetupStep(step="trading_preferences", completed=True),
                SetupStep(step="account_funding", completed=True),
                SetupStep(step="confirmation", completed=True)
            ]
        )
    
    # Get or create wizard state
    return get_or_create_wizard_state(current_user.id)

class ProfileSetupData(BaseModel):
    full_name: str
    preferred_currency: str = "USD"

@router.post("/profile", response_model=SetupWizardStatus)
async def setup_profile(profile_data: ProfileSetupData, current_user: User = Depends(get_current_user)):
    # Update user profile
    user_update = UserUpdate(full_name=profile_data.full_name)
    update_user(current_user.id, user_update.dict(exclude_unset=True))
    
    # Update wizard state
    wizard_state = get_or_create_wizard_state(current_user.id)
    for step in wizard_state.steps:
        if step.step == "profile":
            step.completed = True
            step.data = profile_data.dict()
    
    wizard_state.current_step = "security"
    setup_wizard_state[current_user.id] = wizard_state
    
    return wizard_state

class SecuritySetupData(BaseModel):
    two_factor_enabled: bool = False
    two_factor_method: str = "none"
    
    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        # Convert string to enum for two_factor_method
        from app.models.user import TwoFactorMethod
        if "two_factor_method" in data:
            data["two_factor_method"] = TwoFactorMethod(data["two_factor_method"])
        return data

@router.post("/security", response_model=SetupWizardStatus)
async def setup_security(security_data: SecuritySetupData, current_user: User = Depends(get_current_user)):
    # Update user security settings
    from app.models.user import TwoFactorMethod
    user_update = UserUpdate(
        two_factor_enabled=security_data.two_factor_enabled,
        two_factor_method=TwoFactorMethod(security_data.two_factor_method)
    )
    update_user(current_user.id, user_update.dict(exclude_unset=True))
    
    # Update wizard state
    wizard_state = get_or_create_wizard_state(current_user.id)
    
    # Check if previous step is completed
    profile_completed = False
    for step in wizard_state.steps:
        if step.step == "profile":
            profile_completed = step.completed
    
    if not profile_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Previous step (profile) not completed"
        )
    
    # Update security step
    for step in wizard_state.steps:
        if step.step == "security":
            step.completed = True
            step.data = security_data.dict()
    
    wizard_state.current_step = "trading_preferences"
    setup_wizard_state[current_user.id] = wizard_state
    
    return wizard_state

class TradingPreferencesData(BaseModel):
    risk_tolerance: str  # low, medium, high
    preferred_assets: List[str]  # crypto, stocks, forex, commodities
    trading_frequency: str  # daily, weekly, monthly
    auto_trading_enabled: bool = False

@router.post("/trading_preferences", response_model=SetupWizardStatus)
async def setup_trading_preferences(preferences_data: TradingPreferencesData, current_user: User = Depends(get_current_user)):
    # Update wizard state
    wizard_state = get_or_create_wizard_state(current_user.id)
    
    # Check if previous steps are completed
    security_completed = False
    for step in wizard_state.steps:
        if step.step == "security":
            security_completed = step.completed
    
    if not security_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Previous step (security) not completed"
        )
    
    # Update trading preferences step
    for step in wizard_state.steps:
        if step.step == "trading_preferences":
            step.completed = True
            step.data = preferences_data.dict()
    
    wizard_state.current_step = "account_funding"
    setup_wizard_state[current_user.id] = wizard_state
    
    return wizard_state

class AccountFundingData(BaseModel):
    initial_deposit: float
    currency: str = "USD"
    
    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        # Convert float to Decimal for initial_deposit
        from decimal import Decimal
        if "initial_deposit" in data:
            data["initial_deposit"] = Decimal(str(data["initial_deposit"]))
        return data

@router.post("/account_funding", response_model=SetupWizardStatus)
async def setup_account_funding(funding_data: AccountFundingData, current_user: User = Depends(get_current_user)):
    # Check if user already has an account
    existing_account = get_account_by_user_id(current_user.id)
    
    if not existing_account:
        # Create account with initial deposit
        from decimal import Decimal
        account_create = AccountCreate(
            user_id=current_user.id,
            initial_deposit=Decimal(str(funding_data.initial_deposit)),
            currency=funding_data.currency
        )
        await create_new_account(account_create, current_user)
    
    # Update wizard state
    wizard_state = get_or_create_wizard_state(current_user.id)
    
    # Check if previous steps are completed
    preferences_completed = False
    for step in wizard_state.steps:
        if step.step == "trading_preferences":
            preferences_completed = step.completed
    
    if not preferences_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Previous step (trading_preferences) not completed"
        )
    
    # Update account funding step
    for step in wizard_state.steps:
        if step.step == "account_funding":
            step.completed = True
            step.data = funding_data.dict()
    
    wizard_state.current_step = "confirmation"
    setup_wizard_state[current_user.id] = wizard_state
    
    return wizard_state

@router.post("/complete", response_model=SetupWizardStatus)
async def complete_setup(current_user: User = Depends(get_current_user)):
    # Update wizard state
    wizard_state = get_or_create_wizard_state(current_user.id)
    
    # Check if all previous steps are completed
    all_steps_completed = True
    for step in wizard_state.steps:
        if step.step != "confirmation" and not step.completed:
            all_steps_completed = False
    
    if not all_steps_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not all steps are completed"
        )
    
    # Mark setup as completed
    user_update = UserUpdate(setup_completed=True)
    update_user(current_user.id, user_update.dict(exclude_unset=True))
    
    # Update confirmation step
    for step in wizard_state.steps:
        if step.step == "confirmation":
            step.completed = True
    
    wizard_state.completed = True
    wizard_state.current_step = "completed"
    setup_wizard_state[current_user.id] = wizard_state
    
    return wizard_state

@router.post("/reset", response_model=SetupWizardStatus)
async def reset_setup(current_user: User = Depends(get_current_user)):
    # Reset setup completion status
    user_update = UserUpdate(setup_completed=False)
    update_user(current_user.id, user_update.dict(exclude_unset=True))
    
    # Reset wizard state
    if current_user.id in setup_wizard_state:
        del setup_wizard_state[current_user.id]
    
    # Return fresh wizard state
    return get_or_create_wizard_state(current_user.id)
