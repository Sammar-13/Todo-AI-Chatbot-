"""Authentication request/response schemas (Task 02-032)."""

from pydantic import BaseModel, EmailStr, Field

from .user import UserRead


class LoginRequest(BaseModel):
    """User login request schema.

    Attributes:
        email: User's email address
        password: User's password
    """

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class RegisterRequest(BaseModel):
    """User registration request schema.

    Attributes:
        email: New user's email address
        password: New user's password (min 8 chars)
        full_name: New user's full name
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


class TokenResponse(BaseModel):
    """Successful authentication token response.

    Attributes:
        access_token: JWT access token for API requests
        refresh_token: JWT refresh token for getting new access tokens
        token_type: Type of token (always "bearer")
        user: User information
    """

    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    user: UserRead = Field(..., description="Authenticated user")


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema.

    Attributes:
        refresh_token: Valid refresh token from previous authentication
    """

    refresh_token: str = Field(..., description="Valid refresh token")


class LogoutResponse(BaseModel):
    """Logout response schema.

    Attributes:
        message: Success message
    """

    message: str = Field(default="Successfully logged out", description="Success message")
