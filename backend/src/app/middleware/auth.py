"""Authentication middleware for cookie-based JWT verification (Task 02-050)."""

from typing import Optional
from uuid import UUID

from fastapi import Request
from jose import JWTError, jwt

from ..config import settings


async def verify_token_from_cookie(request: Request) -> Optional[dict]:
    """Extract and verify JWT token from HTTP-only cookie.

    Args:
        request: FastAPI Request object containing cookies

    Returns:
        Token payload dict if valid, None otherwise

    Security:
        - Validates JWT signature with SECRET_KEY
        - Checks token type is "access"
        - Returns None on any verification failure (no exceptions)
    """
    # Extract access_token from cookies
    token = request.cookies.get("access_token")
    if not token:
        return None

    try:
        # Verify JWT signature and expiration
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )

        # Verify token type is "access" (not "refresh")
        if payload.get("type") != "access":
            return None

        return payload
    except JWTError:
        # Invalid signature, expired, or malformed
        return None
    except Exception:
        # Any other error
        return None


async def get_user_id_from_cookie(request: Request) -> Optional[str]:
    """Extract user ID from access token in cookie.

    Args:
        request: FastAPI Request object

    Returns:
        User ID string if token is valid, None otherwise
    """
    payload = await verify_token_from_cookie(request)
    if not payload:
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    return user_id
