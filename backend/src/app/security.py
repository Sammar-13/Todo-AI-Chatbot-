"""Security utilities for password hashing and JWT token handling (Tasks 02-013, 02-014, 02-015)."""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from uuid import UUID

from jose import JWTError, jwt
import bcrypt

from .config import settings


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt (Task 02-013).

    Args:
        password: Plaintext password to hash

    Returns:
        Bcrypt hashed password

    Raises:
        ValueError: If password is empty or invalid
    """
    if not password:
        raise ValueError("Password cannot be empty")

    # Bcrypt has a maximum password length of 72 bytes.
    # We truncate the password to ensure it doesn't cause errors.
    password_bytes = password.encode("utf-8")[:72]

    salt = bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its hash (Task 02-014).

    Args:
        plain_password: Plaintext password to verify
        hashed_password: Previously hashed password to compare against

    Returns:
        True if password matches hash, False otherwise
    """
    if not plain_password:
        return False

    # Truncate to 72 bytes as per bcrypt limits
    password_bytes = plain_password.encode("utf-8")[:72]

    try:
        return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))
    except Exception:
        return False


def create_access_token(data: Dict[str, Any]) -> str:
    """Create JWT access token with 24-hour expiration (Task 02-015).

    Args:
        data: Dictionary with token claims (should include 'sub' for user ID)

    Returns:
        Encoded JWT token string

    Raises:
        ValueError: If data is empty or missing required fields
    """
    if not data:
        raise ValueError("Token data cannot be empty")

    to_encode = data.copy()

    # Add expiration time (24 hours from now)
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire, "type": "access"})

    try:
        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        return encoded_jwt
    except Exception as e:
        raise ValueError(f"Failed to create access token: {e}") from e


def create_refresh_token(user_id: UUID) -> str:
    """Create JWT refresh token with 7-day expiration (Task 02-015).

    Args:
        user_id: UUID of the user

    Returns:
        Encoded JWT refresh token string

    Raises:
        ValueError: If user_id is invalid
    """
    if not user_id:
        raise ValueError("User ID cannot be empty")

    to_encode = {
        "sub": str(user_id),
        "type": "refresh",
    }

    # Add expiration time (7 days from now)
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})

    try:
        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        return encoded_jwt
    except Exception as e:
        raise ValueError(f"Failed to create refresh token: {e}") from e


def verify_token(token: str) -> Dict[str, Any]:
    """Verify JWT token and return payload (Task 02-015).

    Args:
        token: JWT token string to verify

    Returns:
        Token payload dictionary

    Raises:
        ValueError: If token is invalid, expired, or verification fails
    """
    if not token:
        raise ValueError("Token cannot be empty")

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError as e:
        raise ValueError(f"Invalid token: {e}") from e
    except Exception as e:
        raise ValueError(f"Token verification failed: {e}") from e


def extract_user_id_from_token(token: str) -> Optional[str]:
    """Extract user ID from JWT token payload.

    Args:
        token: JWT token string

    Returns:
        User ID string if valid, None otherwise
    """
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        return user_id
    except ValueError:
        return None
