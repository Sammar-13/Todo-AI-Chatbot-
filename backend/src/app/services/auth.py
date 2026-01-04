"""Authentication service with business logic (Task 02-031)."""

from typing import Optional, Tuple
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..db.models import RefreshToken, User
from ..security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)


async def register_user(
    session: AsyncSession,
    email: str,
    password: str,
    full_name: str,
) -> User:
    """Register a new user with email and password (Task 02-031).

    Args:
        session: Database session
        email: User's email address
        password: Plaintext password
        full_name: User's full name

    Returns:
        Created User object

    Raises:
        ValueError: If email already exists or validation fails
    """
    if not email or not password or not full_name:
        raise ValueError("Email, password, and full name are required")

    # Check if email already exists
    result = await session.execute(select(User).where(User.email == email))
    existing = result.scalars().first()
    if existing:
        raise ValueError(f"Email {email} is already registered")

    # Generate username from email
    username = email.split("@")[0]
    counter = 1
    base_username = username
    
    while True:
        result = await session.execute(select(User).where(User.username == username))
        if not result.scalars().first():
            break
        username = f"{base_username}{counter}"
        counter += 1

    # Hash password
    password_hash = hash_password(password)

    # Create user
    user = User(
        email=email,
        username=username,
        password_hash=password_hash,
        full_name=full_name,
        is_active=True,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def authenticate_user(
    session: AsyncSession,
    email: str,
    password: str,
) -> Optional[User]:
    """Authenticate user with email and password (Task 02-031).

    Args:
        session: Database session
        email: User's email address
        password: Plaintext password to verify

    Returns:
        User object if credentials valid, None otherwise
    """
    if not email or not password:
        return None

    # Find user by email
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    user = result.scalars().first()

    if not user:
        return None

    # Verify password
    if not verify_password(password, user.password_hash):
        return None

    # Check if user is active
    if not user.is_active:
        return None

    return user


async def create_tokens(
    session: AsyncSession,
    user_id: UUID,
) -> Tuple[str, str]:
    """Create access and refresh tokens for user (Task 02-031).

    Args:
        session: Database session
        user_id: UUID of user

    Returns:
        Tuple of (access_token, refresh_token)

    Raises:
        ValueError: If token creation fails
    """
    # Create access token
    access_token = create_access_token({"sub": str(user_id)})

    # Create refresh token
    refresh_token = create_refresh_token(user_id)

    # Store refresh token in database
    db_refresh_token = RefreshToken(
        user_id=user_id,
        token=refresh_token,
    )

    session.add(db_refresh_token)
    await session.commit()

    return access_token, refresh_token


async def validate_email_unique(session: AsyncSession, email: str) -> bool:
    """Check if email is unique (not already registered) (Task 02-031).

    Args:
        session: Database session
        email: Email address to check

    Returns:
        True if email is unique, False if already exists
    """
    if not email:
        return False

    result = await session.execute(select(User).where(User.email == email))
    existing = result.scalars().first()
    return existing is None