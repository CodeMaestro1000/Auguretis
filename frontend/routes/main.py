from fastapi import APIRouter
from routes.user_routes import frontend_users_router
from routes.app_routes import app_router


frontend_router = APIRouter()

frontend_router.include_router(frontend_users_router, tags=["users"])
frontend_router.include_router(app_router, prefix="/app", tags=["apps"])