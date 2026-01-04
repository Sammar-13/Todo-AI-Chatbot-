"""FastAPI dependency injection functions (Task 02-019)."""

from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status, Header, Request
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .database import get_session
from .db.models import User
from .security import extract_user_id_from_token


def _extract_token(
    request: Request,
    authorization: Optional[str] = Header(None)
) -> str:
    """Extract JWT token from cookies or Authorization header.

    Checks for token in this order:
    1. HTTP-only cookie (access_token)
    2. Authorization header (Bearer token)

    Args:
        request: FastAPI request object for cookie access
        authorization: Authorization header value

    Returns:
        JWT token string

    Raises:
        HTTPException: 401 if no token found or format is invalid
    """
    # Debug: Print all cookies
    print(f"[DEBUG] _extract_token: Cookies received: {request.cookies.keys()}")
    
    # First, try to get token from cookies (HTTP-only)
    token_from_cookie = request.cookies.get("access_token")
    if token_from_cookie:
        print("[DEBUG] _extract_token: Found access_token in cookies")
        return token_from_cookie

    # Fall back to Authorization header
    if not authorization:
        print("[DEBUG] _extract_token: No access_token in cookies and no Authorization header")
        return ""

    # Expected format: "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        print("[DEBUG] _extract_token: Invalid Authorization header format")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print("[DEBUG] _extract_token: Found token in Authorization header")
    return parts[1]


async def get_current_user(
    token: str = Depends(_extract_token),
    session: AsyncSession = Depends(get_session),
) -> User:
    """Get current authenticated user from JWT token (Task 02-019).

    Extracts user ID from JWT token, validates it exists and is active,
    and returns the User object.

    Args:
        token: JWT token from Authorization header
        session: Database session

    Returns:
        Authenticated User object

    Raises:
        HTTPException: 401 if token is invalid/expired, 403 if user inactive, 404 if not found
    """
    try:
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Extract user ID from token
        user_id_str = extract_user_id_from_token(token)
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Validate UUID format
        try:
            user_id = UUID(user_id_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Query user from database
        print(f"[DEBUG] get_current_user: Querying user {user_id}")
        statement = select(User).where(User.id == user_id)
        result = await session.execute(statement)
        user = result.scalars().first()

        if not user:
            print(f"[DEBUG] get_current_user: User {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if not user.is_active:
            print(f"[DEBUG] get_current_user: User {user_id} is inactive")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        print(f"[DEBUG] get_current_user: Successfully retrieved user {user_id}")
        return user

    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] get_current_user: Unexpected error: {e}")
        import traceback
        print(f"[TRACEBACK]\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e