from fastapi import APIRouter

from cms.api import user
api_router = APIRouter()
api_router.include_router(user.router, tags=["用户管理"])
