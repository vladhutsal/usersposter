from fastapi import APIRouter

from app.api.endpoints import analytics, users, posts

api_router = APIRouter()
api_router.include_router(users.router, prefix='/users', tags=['user'])
api_router.include_router(posts.router, prefix='/posts', tags=['posts'])
api_router.include_router(analytics.router, prefix='/analytics', tags=['analytics'])
