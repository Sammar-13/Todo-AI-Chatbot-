"""Authentication API routes (Tasks 02-016, 02-017, 02-018, 02-020, 02-021, 02-050)."""

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlmodel.ext.asyncio.session import AsyncSession

from ...database import get_session
from ...schemas import LoginRequest, RegisterRequest, TokenResponse, UserRead
from ...services.auth import (
    authenticate_user,
    create_tokens,
    register_user,
    validate_email_unique,
)
from ..dependencies import get_current_user
from ...db.models import User
from ...config import settings
from ...middleware.auth import verify_token_from_cookie

router = APIRouter(prefix="/auth", tags=["authentication"])


def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    """Set HTTP-only authentication cookies on response.

    Args:
        response: FastAPI Response object
        access_token: JWT access token
        refresh_token: JWT refresh token

    Security:
        - httponly=True: Prevents JavaScript access (XSS protection)
        - secure=True in production: HTTPS only (MITM protection)
        - samesite="lax": CSRF protection for safe cross-site requests
        - max_age: Access token 24h, refresh token 7 days
    """
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=86400,  # 24 hours
        httponly=True,
        secure=settings.is_production,  # HTTPS only in production
        samesite="lax",
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=604800,  # 7 days
        httponly=True,
        secure=settings.is_production,  # HTTPS only in production
        samesite="lax",
        path="/",
    )


def clear_auth_cookies(response: Response) -> None:
    """Clear authentication cookies from response.

    Args:
        response: FastAPI Response object
    """
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    """Register a new user with email and password (Task 02-016).

    Args:
        request: Registration request with email, password, full_name
        response: FastAPI Response to set cookies
        session: Database session

    Returns:
        TokenResponse with access_token, refresh_token, and user info

    Raises:
        HTTPException: 400 if email exists or validation fails
    """
    print(f"[DEBUG] Register endpoint hit for email: {request.email}")
    try:
        # Validate email is unique
        if not await validate_email_unique(session, request.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Create user
        user = await register_user(
            session,
            email=request.email,
            password=request.password,
            full_name=request.full_name,
        )

        # Create tokens
        access_token, refresh_token = await create_tokens(session, user.id)

        # Set HTTP-only cookies
        set_auth_cookies(response, access_token, refresh_token)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserRead.model_validate(user),
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback_msg = traceback.format_exc()
        print(f"[ERROR] Registration failed with {type(e).__name__}: {error_msg}")
        print(f"[TRACEBACK]\n{traceback_msg}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {error_msg}",
        ) from e


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    """Login user with email and password (Task 02-017).

    Args:
        request: Login request with email and password
        response: FastAPI Response to set cookies
        session: Database session

    Returns:
        TokenResponse with access_token, refresh_token, and user info

    Raises:
        HTTPException: 401 if credentials are invalid
    """
    try:
        # Authenticate user
        user = await authenticate_user(session, request.email, request.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create tokens
        access_token, refresh_token = await create_tokens(session, user.id)

        # Set HTTP-only cookies
        set_auth_cookies(response, access_token, refresh_token)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserRead.model_validate(user),
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create tokens",
        ) from e
    except Exception as e:
        with open("login_errors.log", "a") as f:
            f.write(f"Login error: {str(e)}\n")
            import traceback
            f.write(traceback.format_exc() + "\n")
        print(f"[ERROR] Login failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is offline. Cannot login. Please try again when database is online.",
        ) from e


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    """Refresh access token using refresh token (Task 02-018).

    Gets refresh token from HTTP-only cookie instead of request body.

    Args:
        request: FastAPI Request (contains cookies)
        response: FastAPI Response to set new cookies
        session: Database session

    Returns:
        TokenResponse with new access_token and refresh_token

    Raises:
        HTTPException: 401 if refresh token is invalid
    """
    # Get refresh_token from cookie
    refresh_token_value = request.cookies.get("refresh_token")
    if not refresh_token_value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        from ...security import verify_token, create_access_token

        payload = verify_token(refresh_token_value)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = await session.get(User, user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create new tokens
        new_access_token = create_access_token({"sub": str(user.id)})
        new_refresh_token = (await create_tokens(session, user.id))[1]

        # Set new cookies
        set_auth_cookies(response, new_access_token, new_refresh_token)

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            user=UserRead.model_validate(user),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    response: Response,
    current_user: User = Depends(get_current_user),
) -> dict:
    """Logout user by clearing authentication cookies (Task 02-020).

    Args:
        response: FastAPI Response to clear cookies
        current_user: Currently authenticated user (validates auth)

    Returns:
        Success message
    """
    # Clear authentication cookies
    clear_auth_cookies(response)
    return {"message": "Successfully logged out"}


@router.get("/verify")
async def verify_session(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Verify current session from HTTP-only cookie (Task 02-050).

    This endpoint is called on app load to verify the user's session
    is still valid. It extracts the access token from cookies and
    verifies it with the database.

    Args:
        request: FastAPI Request (contains cookies)
        session: Database session

    Returns:
        Dict with:
        - authenticated: bool - Whether user is authenticated
        - user: UserRead - User info if authenticated, None otherwise

    Security:
        - Token extracted from HTTP-only cookie (not accessible by JS)
        - Token verified server-side
        - Database lookup confirms user still exists and is active
    """
    # Verify token from cookie
    payload = await verify_token_from_cookie(request)
    if not payload:
        return {"authenticated": False, "user": None}

    # Get user from database
    try:
        user_id = payload.get("sub")
        if not user_id:
            return {"authenticated": False, "user": None}

        from uuid import UUID
        user_uuid = UUID(user_id)
        user = await session.get(User, user_uuid)
        if not user or not user.is_active:
            return {"authenticated": False, "user": None}

        return {
            "authenticated": True,
            "user": UserRead.model_validate(user),
        }
    except Exception as e:
        print(f"[ERROR] Session verification failed: {str(e)}")
        return {"authenticated": False, "user": None}


@router.get("/me", response_model=UserRead)
async def get_current_user_endpoint(
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """Get current authenticated user (Task 02-021).

    Args:
        current_user: Currently authenticated user

    Returns:
        UserRead with current user information
    """
    return UserRead.model_validate(current_user)