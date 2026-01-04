"""User request/response schemas (Task 02-032)."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """User creation request schema.

    Attributes:
        email: User's email address
        password: Plaintext password (min 8 chars)
        full_name: User's full name
    """

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password (minimum 8 characters)",
    )
    full_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="User's full name",
    )


class UserRead(BaseModel):
    """User read response schema.

    Attributes:
        id: User's unique identifier
        email: User's email address
        full_name: User's full name
        avatar_url: Optional profile picture URL
        is_active: Whether user account is active
        created_at: Account creation timestamp
    """

    id: UUID = Field(..., description="Unique user ID")
    email: str = Field(..., description="User's email")
    full_name: str = Field(..., description="User's full name")
    avatar_url: Optional[str] = Field(None, description="Profile picture URL")
    is_active: bool = Field(..., description="Account active status")
    created_at: datetime = Field(..., description="Account creation time")

    class Config:
        """Pydantic config."""

        from_attributes = True


class UserUpdate(BaseModel):
    """User update request schema.

    All fields are optional - only provided fields will be updated.

    Attributes:
        full_name: Updated full name
        avatar_url: Updated profile picture URL
    """

    full_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Updated full name",
    )
    avatar_url: Optional[str] = Field(
        None,
        max_length=2048,
        description="Updated profile picture URL",
    )


class UserProfile(BaseModel):
    """User profile response schema with additional details.

    Attributes:
        id: User's unique identifier
        email: User's email address
        username: User's username
        full_name: User's full name
        avatar_url: Optional profile picture URL
        is_active: Whether user account is active
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """

    id: UUID = Field(..., description="Unique user ID")
    email: str = Field(..., description="User's email")
    username: str = Field(..., description="User's username")
    full_name: str = Field(..., description="User's full name")
    avatar_url: Optional[str] = Field(None, description="Profile picture URL")
    is_active: bool = Field(..., description="Account active status")
    created_at: datetime = Field(..., description="Account creation time")
    updated_at: datetime = Field(..., description="Last update time")

    class Config:
        """Pydantic config."""

        from_attributes = True
