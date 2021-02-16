from fastapi import APIRouter

from backend.api.endpoints import analytics, users, posts


api_router = APIRouter()
api_router.include_router(users.router, prefix='/users', tags=['Users'])
api_router.include_router(posts.router, prefix='/posts', tags=['Posts'])
api_router.include_router(analytics.router, prefix='/analytics', tags=['Analytics'])
