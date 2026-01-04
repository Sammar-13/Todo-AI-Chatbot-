"""User database model (Task 02-026)."""

from typing import Optional

from sqlmodel import Field, SQLModel

from .base import BaseModel


class User(BaseModel, table=True):
    """User model for authentication and profile management.

    Stores user account information including credentials and profile details.
    All users must have a unique email and username.

    Attributes:
        email: User's email address (unique)
        username: User's username for login (unique)
        password_hash: Hashed password for authentication
        full_name: User's full name
        avatar_url: Optional URL to user's profile picture
        is_active: Whether the user account is active
    """

    __tablename__ = "users"

    email: str = Field(
        unique=True,
        index=True,
        min_length=5,
        max_length=255,
        description="User's unique email address",
    )
    username: str = Field(
        unique=True,
        index=True,
        min_length=3,
        max_length=50,
        description="User's unique username",
    )
    password_hash: str = Field(min_length=60, description="Bcrypt hashed password")
    full_name: str = Field(max_length=255, description="User's full name")
    avatar_url: Optional[str] = Field(
        default=None,
        max_length=2048,
        description="URL to user's profile picture",
    )
    is_active: bool = Field(default=True, description="Whether user account is active")
