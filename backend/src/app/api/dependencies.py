"""API-level dependencies."""

from fastapi import Depends, Header
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from ..dependencies import get_current_user as get_current_user_dependency
from ..dependencies import _extract_token
from ..database import get_session
from ..db.models import User


async def get_current_user(
    token: str = Depends(_extract_token),
    session: AsyncSession = Depends(get_session),
) -> User:
    """Get current authenticated user from JWT token.

    This is the API-level wrapper that properly chains the token extraction
    and database session dependencies.

    Args:
        token: JWT token from Authorization header
        session: Database session from dependency injection

    Returns:
        Authenticated User object

    Raises:
        HTTPException: 401 if token invalid, 403 if inactive, 404 if not found
    """
    return await get_current_user_dependency(token=token, session=session)
