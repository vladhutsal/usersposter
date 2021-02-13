from fastapi import APIRouter

from app.endpoints import users, login

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=['login'])
api_router.include_router(users.router, prefix="/users", tags=['user'])
