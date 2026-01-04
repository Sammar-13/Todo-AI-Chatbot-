"""Health check API route (Task 02-042)."""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlmodel.ext.asyncio.session import AsyncSession

from ...database import get_session

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check() -> dict:
    """Health check endpoint (Task 02-042).

    Returns:
        Status response indicating service is healthy
    """
    return {"status": "healthy"}


@router.get("/db")
async def health_check_db(session: AsyncSession = Depends(get_session)) -> dict:
    """Health check endpoint for database connection.

    Returns:
        Status response with database connection status
    """
    try:
        result = await session.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {
            "status": "error",
            "database": "disconnected",
            "error": str(e),
        }
