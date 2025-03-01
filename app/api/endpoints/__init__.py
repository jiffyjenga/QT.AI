from fastapi import APIRouter
from app.api.endpoints import users, accounts, setup

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(setup.router, prefix="/setup", tags=["setup"])
