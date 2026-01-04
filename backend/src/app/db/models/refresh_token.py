"""Refresh token database model."""

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import BaseModel


class RefreshToken(BaseModel, table=True):
    """Refresh token model for JWT token rotation.

    Stores refresh tokens for users to enable long-lived sessions
    with periodic token rotation for security.

    Attributes:
        user_id: ID of the user who owns this refresh token
        token: The actual JWT refresh token (unique)
        expires_at: When this refresh token expires
    """

    __tablename__ = "refresh_tokens"

    user_id: UUID = Field(
        foreign_key="users.id",
        index=True,
        description="ID of the token owner",
    )
    token: str = Field(
        unique=True,
        index=True,
        description="JWT refresh token",
    )
    expires_at: datetime = Field(
        default_factory=lambda: (datetime.now(timezone.utc) + timedelta(days=7)).replace(tzinfo=None),
        description="Token expiration timestamp",
    )
