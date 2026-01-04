"""API v1 routes package."""

from fastapi import APIRouter

from .auth import router as auth_router
from .health import router as health_router
from .tasks import router as tasks_router
from .users import router as users_router

# Create API router
api_router = APIRouter(prefix="/api/v1")

# Include all sub-routers
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(tasks_router)

__all__ = ["api_router"]
