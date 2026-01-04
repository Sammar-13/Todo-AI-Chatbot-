# Authentication Persistence Issue - Complete Analysis & Solution

**Current Issue**: User is redirected to login/signup page after page refresh, losing session

**Goal**: Keep user logged in after refresh and remain on dashboard

---

## Part 1: Why This Issue Happens

### Current Implementation Problem

```
┌─────────────────────────────────────────────────────────────┐
│                     CURRENT FLOW (BROKEN)                    │
└─────────────────────────────────────────────────────────────┘

1. USER LOGS IN
   Login Form → Backend validates → Returns JWT tokens → Frontend stores in localStorage

2. EVERYTHING WORKS
   User on /tasks page, has access_token in localStorage

3. USER PRESSES F5 (REFRESH)
   ❌ Page reloads, React app restarts
   ❌ localStorage is empty on initial render (not loaded yet)
   ❌ AuthContext checks for token, finds none
   ❌ isAuthenticated = false
   ❌ Dashboard layout redirects to /login
   ⏱️ After 100ms, localStorage loads and token is found
   ✓ But too late - user already on login page

4. RESULT
   User bounces from /tasks → /login even though token still exists
```

### Root Cause Analysis

**Problem 1: Race Condition in Token Loading**
```typescript
// CURRENT PROBLEMATIC CODE
const [state, setState] = useState(defaultAuthState) // isAuthenticated = false

useEffect(() => {
  const token = apiClient.getAccessToken() // Async operation
  if (token) {
    // Try to load user...
  }
}, [])

// Component renders BEFORE useEffect runs
// isAuthenticated is false during initial render
// Dashboard layout sees isAuthenticated = false
// Redirects to /login
// THEN useEffect loads token
// But redirect already happened!
```

**Problem 2: localStorage Not Available During SSR/Initial Render**
```typescript
// Server-side rendering/hydration mismatch
const token = localStorage.getItem('access_token') // window is undefined on server
// Results in hydration mismatch and token not loading on first render
```

**Problem 3: No Server-Side Session Verification**
- Backend doesn't verify session on initial page load
- Frontend relies entirely on localStorage (not secure)
- No way to validate token on server-side

---

## Part 2: Best-Practice Solution

### Strategy Overview

```
┌──────────────────────────────────────────────────────────────┐
│              SOLUTION: HYBRID APPROACH                        │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│ 1. USE HTTP-ONLY COOKIES (SERVER SETS)                       │
│    • Access token → HTTP-only cookie (secure, not accessible │
│    • Refresh token → HTTP-only cookie (secure)               │
│    • Browser auto-sends on every request                      │
│    • Cannot be stolen via XSS                                │
│                                                                │
│ 2. VERIFY SESSION ON SERVER                                  │
│    • Middleware checks cookie on every request               │
│    • Validates JWT signature and expiration                  │
│    • Returns user data if valid                              │
│                                                                │
│ 3. SYNC INITIAL STATE ON FRONTEND LOAD                       │
│    • Get /api/auth/verify endpoint called on app start       │
│    • If cookie valid → Backend returns user data             │
│    • Frontend sets isAuthenticated = true                    │
│    • No redirect happens                                      │
│                                                                │
│ 4. PROTECT ROUTES                                             │
│    • Dashboard routes: Show if authenticated                 │
│    • Login/Signup routes: Redirect if already authenticated  │
│    • Public routes: Show always                              │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

### Token Storage Comparison

| Strategy | Security | XSS Proof | CSRF Proof | Refresh | Notes |
|----------|----------|-----------|-----------|---------|-------|
| **localStorage** | ❌ Low | ❌ No | ❌ No | Manual | Current (vulnerable) |
| **sessionStorage** | ❌ Low | ❌ No | ❌ No | Manual | Only per tab |
| **HTTP-only Cookie** | ✅ High | ✅ Yes | ⚠️ Needs CSRF token | Auto | **RECOMMENDED** |
| **Secure Cookie** | ✅ High | ✅ Yes | ⚠️ Needs CSRF token | Auto | Same as HTTP-only + HTTPS only |
| **Memory** | ✅ High | ✅ Yes | ✅ Yes | Manual | Lost on refresh (bad UX) |

### Recommended: HTTP-Only Cookies

**Why HTTP-Only Cookies?**
1. ✅ Cannot be accessed by JavaScript (XSS safe)
2. ✅ Automatically sent by browser on every request
3. ✅ Server can validate immediately
4. ✅ Survives page refresh
5. ⚠️ Requires CSRF protection (but we have it)

---

## Part 3: Implementation

### BACKEND CHANGES

#### Step 1: Create Cookie-Based Auth Middleware

**File**: `backend/src/app/middleware/auth.py` (NEW FILE)

```python
"""Authentication middleware for cookie-based JWT"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Request, HTTPException, status
from jose import JWTError, jwt
from functools import wraps

from ..config import settings

async def verify_token_from_cookie(request: Request) -> Optional[dict]:
    """
    Verify JWT token from HTTP-only cookie

    Returns:
        dict with user_id if valid
        None if no token or invalid
    """
    token = request.cookies.get("access_token")

    if not token:
        return None

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        # Check token type
        if payload.get("type") != "access":
            return None

        return payload

    except JWTError:
        return None


async def require_auth_cookie(request: Request) -> dict:
    """
    Dependency: Require valid token in cookie

    Raises:
        HTTPException: 401 if no valid token
    """
    payload = await verify_token_from_cookie(request)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload
```

#### Step 2: Add Cookie Response Headers to Auth Endpoints

**File**: `backend/src/app/api/v1/auth.py` (MODIFY)

```python
from fastapi import APIRouter, Response
from datetime import datetime, timedelta, timezone
import json

router = APIRouter(prefix="/auth", tags=["authentication"])

def set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    """Set HTTP-only cookies for authentication tokens"""

    # Access token: expires in 24 hours
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=86400,  # 24 hours in seconds
        httponly=True,  # Cannot be accessed by JavaScript
        secure=settings.is_production,  # HTTPS only in production
        samesite="lax",  # CSRF protection
        path="/",
    )

    # Refresh token: expires in 7 days
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=604800,  # 7 days in seconds
        httponly=True,
        secure=settings.is_production,
        samesite="lax",
        path="/",
    )


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    """Register a new user with HTTP-only cookies"""
    try:
        # ... existing validation code ...

        user = await register_user(session, email=request.email, password=request.password, full_name=request.full_name)
        access_token, refresh_token = await create_tokens(session, user.id)

        # SET COOKIES
        set_auth_cookies(response, access_token, refresh_token)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserRead.model_validate(user),
        )
    except Exception as e:
        # ... error handling ...
        raise


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    """Login user with HTTP-only cookies"""
    try:
        user = await authenticate_user(session, request.email, request.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token, refresh_token = await create_tokens(session, user.id)

        # SET COOKIES
        set_auth_cookies(response, access_token, refresh_token)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserRead.model_validate(user),
        )
    except Exception as e:
        raise


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    """Refresh access token using refresh token from cookie"""

    refresh_token_value = request.cookies.get("refresh_token")
    if not refresh_token_value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found",
        )

    try:
        payload = jwt.decode(
            refresh_token_value,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        user_id = payload.get("sub")
        new_access_token, new_refresh_token = await create_tokens(session, UUID(user_id))

        # SET NEW COOKIES
        set_auth_cookies(response, new_access_token, new_refresh_token)

        user = await session.get(User, UUID(user_id))
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            user=UserRead.model_validate(user),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


@router.post("/logout")
async def logout(response: Response):
    """Logout user by clearing cookies"""
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")
    return {"message": "Logged out successfully"}
```

#### Step 3: Add Verification Endpoint

**File**: `backend/src/app/api/v1/auth.py` (ADD NEW ENDPOINT)

```python
@router.get("/verify", response_model=dict)
async def verify_session(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Verify current session from cookie

    Called on frontend app load to restore session
    Returns:
        - {authenticated: true, user: {...}} if valid cookie
        - {authenticated: false} if no valid cookie
    """
    payload = await verify_token_from_cookie(request)

    if not payload:
        return {"authenticated": False}

    try:
        user_id = UUID(payload.get("sub"))
        user = await session.get(User, user_id)

        if not user or not user.is_active:
            return {"authenticated": False}

        return {
            "authenticated": True,
            "user": UserRead.model_validate(user),
        }
    except Exception:
        return {"authenticated": False}
```

#### Step 4: Update Dependencies for Cookie-Based Auth

**File**: `backend/src/app/api/dependencies.py` (MODIFY)

```python
from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from ..database import get_session
from ..middleware.auth import verify_token_from_cookie
from ..db.models import User


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> User:
    """
    Get current user from cookie-based authentication

    Raises:
        HTTPException: 401 if no valid token in cookie
    """
    payload = await verify_token_from_cookie(request)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    from uuid import UUID
    user = await session.get(User, UUID(user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user
```

---

### FRONTEND CHANGES

#### Step 1: Update API Client to Use Cookies

**File**: `frontend/src/utils/api.ts` (MODIFY)

```typescript
class APIClient {
  constructor(baseURL: string = API_URL) {
    this.baseURL = baseURL
    // Cookies are automatically sent - no manual token loading needed
  }

  async fetchAPI<T = unknown>(
    endpoint: string,
    options: FetchOptions = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`
    const fetchOptions: RequestInit = {
      ...options,
      // CRITICAL: Include cookies in requests
      credentials: "include",
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      signal: AbortSignal.timeout(30000),
    }

    try {
      const response = await fetch(url, fetchOptions)

      // Handle 401 - token expired
      if (response.status === 401 && !options.skipRefresh) {
        try {
          // Try to refresh using refresh token from cookie
          const refreshResponse = await fetch(`${this.baseURL}/auth/refresh`, {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
          })

          if (refreshResponse.ok) {
            // Retry original request with new token
            const retryResponse = await fetch(url, fetchOptions)
            return this.parseResponse<T>(retryResponse)
          } else {
            // Refresh failed - redirect to login
            if (typeof window !== 'undefined') {
              window.location.href = '/login'
            }
            throw new APIErrorResponse('Session expired', 'AUTH_EXPIRED', 401)
          }
        } catch (error) {
          if (typeof window !== 'undefined') {
            window.location.href = '/login'
          }
          throw error
        }
      }

      if (!response.ok) {
        await this.handleErrorResponse(response)
      }

      return this.parseResponse<T>(response)
    } catch (error) {
      // ... error handling ...
      throw new APIErrorResponse('Network error', 'NETWORK_ERROR', 0, error)
    }
  }

  // REMOVED: setToken, getAccessToken, getRefreshToken (not needed with cookies)
  // Tokens are managed by browser automatically
}
```

#### Step 2: Update AuthContext for Session Verification

**File**: `frontend/src/context/AuthContext.tsx` (REWRITE)

```typescript
'use client'

import React, { createContext, useCallback, useEffect, useState } from 'react'
import authService from '@/services/auth'
import { AuthState, User, LoginInput, SignUpInput, ApiError } from '@/types'
import apiClient from '@/utils/api'

interface AuthContextType extends AuthState {
  signup: (data: SignUpInput) => Promise<void>
  login: (data: LoginInput) => Promise<void>
  logout: () => Promise<void>
}

const defaultAuthState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: true,  // Start as true - checking session
  error: null,
  tokens: { accessToken: null, refreshToken: null },
}

export const AuthContext = createContext<AuthContextType>({
  ...defaultAuthState,
  signup: async () => {},
  login: async () => {},
  logout: async () => {},
})

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<AuthState>(defaultAuthState)
  const [initialized, setInitialized] = useState(false)

  /**
   * Initialize authentication on app load
   * Verifies session with backend using cookies
   */
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        // Call /api/auth/verify - backend checks cookies
        const response = await fetch('/api/auth/verify', {
          method: 'GET',
          credentials: 'include',  // Include cookies
          headers: { 'Content-Type': 'application/json' },
        })

        const data = await response.json()

        if (data.authenticated && data.user) {
          // Session valid - user stays logged in
          setState({
            user: data.user,
            isAuthenticated: true,
            isLoading: false,
            error: null,
            tokens: { accessToken: null, refreshToken: null },
          })
        } else {
          // No valid session
          setState({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
            tokens: { accessToken: null, refreshToken: null },
          })
        }
      } catch (error) {
        // Error checking session - assume not authenticated
        setState({
          user: null,
          isAuthenticated: false,
          isLoading: false,
          error: error instanceof Error ? { message: error.message } : null,
          tokens: { accessToken: null, refreshToken: null },
        })
      } finally {
        setInitialized(true)
      }
    }

    if (!initialized) {
      initializeAuth()
    }
  }, [initialized])

  /**
   * Handle user signup
   */
  const signup = useCallback(async (data: SignUpInput) => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }))

    try {
      const response = await authService.signup(data)

      // Response includes user - cookies set by backend
      setState((prev) => ({
        ...prev,
        user: response.user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      }))
    } catch (error) {
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? { message: error.message } : error,
      }))
      throw error
    }
  }, [])

  /**
   * Handle user login
   */
  const login = useCallback(async (data: LoginInput) => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }))

    try {
      const response = await authService.login(data)

      // Response includes user - cookies set by backend
      setState((prev) => ({
        ...prev,
        user: response.user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      }))
    } catch (error) {
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? { message: error.message } : error,
      }))
      throw error
    }
  }, [])

  /**
   * Handle user logout
   */
  const logout = useCallback(async () => {
    setState((prev) => ({ ...prev, isLoading: true }))

    try {
      await authService.logout()
      // Backend clears cookies
      setState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
        tokens: { accessToken: null, refreshToken: null },
      })
    } catch (error) {
      // Even if logout fails, clear frontend state
      setState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
        tokens: { accessToken: null, refreshToken: null },
      })
    }
  }, [])

  const value: AuthContextType = {
    ...state,
    signup,
    login,
    logout,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
```

#### Step 3: Create Protected Route Component

**File**: `frontend/src/components/ProtectedRoute.tsx` (NEW)

```typescript
'use client'

import { useAuth } from '@/hooks/useAuth'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
import LoadingSpinner from './LoadingSpinner'

interface ProtectedRouteProps {
  children: React.ReactNode
  requireAuth?: boolean  // true = must be logged in, false = must NOT be logged in
}

export function ProtectedRoute({
  children,
  requireAuth = true
}: ProtectedRouteProps) {
  const { isAuthenticated, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (isLoading) return  // Still checking session

    if (requireAuth && !isAuthenticated) {
      // Page requires auth but user not logged in
      router.push('/login')
    } else if (!requireAuth && isAuthenticated) {
      // Page requires NOT being auth (login/signup) but user IS logged in
      router.push('/tasks')
    }
  }, [isAuthenticated, isLoading, requireAuth, router])

  if (isLoading) {
    return <LoadingSpinner />
  }

  // Check again before rendering
  if (requireAuth && !isAuthenticated) {
    return null  // Will redirect
  }

  if (!requireAuth && isAuthenticated) {
    return null  // Will redirect
  }

  return <>{children}</>
}
```

#### Step 4: Update Layout to Use Protected Routes

**File**: `frontend/src/app/(dashboard)/layout.tsx` (MODIFY)

```typescript
'use client'

import { ReactNode } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { ProtectedRoute } from '@/components/ProtectedRoute'
import Navigation from '@/components/Layout/Navigation'
import Sidebar from '@/components/Layout/Sidebar'

export default function DashboardLayout({ children }: { children: ReactNode }) {
  const { isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-lg text-gray-600">Loading...</div>
      </div>
    )
  }

  return (
    <ProtectedRoute requireAuth={true}>
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        <div className="flex">
          <Sidebar />
          <main className="flex-1 p-6">{children}</main>
        </div>
      </div>
    </ProtectedRoute>
  )
}
```

#### Step 5: Protect Login/Signup Pages

**File**: `frontend/src/app/(auth)/layout.tsx` (NEW)

```typescript
'use client'

import { ReactNode } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { ProtectedRoute } from '@/components/ProtectedRoute'

export default function AuthLayout({ children }: { children: ReactNode }) {
  const { isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-lg text-gray-600">Loading...</div>
      </div>
    )
  }

  return (
    <ProtectedRoute requireAuth={false}>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="flex items-center justify-center min-h-screen px-4">
          <div className="w-full max-w-md">
            {children}
          </div>
        </div>
      </div>
    </ProtectedRoute>
  )
}
```

---

## Part 4: Complete Flow After Implementation

### User Logs In

```
1. User on /login page
2. Enters credentials → Submit
3. Frontend POST /api/auth/login with credentials
4. Backend validates → Returns tokens + sets HTTP-only cookies
5. Frontend receives response → Sets AuthContext (isAuthenticated = true)
6. Redirects to /tasks ✓
```

### User Refreshes Page

```
1. User presses F5 on /tasks page
2. App reinitializes
3. AuthProvider mounts → useEffect runs
4. Calls GET /api/auth/verify
5. Browser auto-sends access_token cookie with request
6. Backend checks cookie → Valid
7. Returns {authenticated: true, user: {...}}
8. Frontend sets state (isAuthenticated = true)
9. DashboardLayout renders without redirect ✓
```

### User Closes & Reopens Browser

```
1. User closes browser completely
2. Opens new browser window
3. Goes to http://localhost:3000
4. App loads → AuthProvider initializes
5. Calls GET /api/auth/verify
6. Browser auto-sends access_token cookie
7. Cookie still valid (24 hour expiration)
8. Backend returns authenticated user
9. Redirects to /tasks automatically ✓
```

### Token Expires

```
1. User on /tasks, access_token about to expire
2. Makes API call (fetch tasks)
3. Backend returns 401 Unauthorized (token expired)
4. API client catches 401
5. Attempts POST /api/auth/refresh
6. Browser sends refresh_token cookie
7. Backend validates refresh token → Issues new access_token
8. Backend sets new HTTP-only cookie
9. API client retries original request
10. Success ✓
```

### User Logs Out

```
1. User clicks "Logout"
2. Frontend calls POST /api/auth/logout
3. Backend deletes cookies and returns success
4. Frontend clears AuthContext state
5. User redirected to /login ✓
```

---

## Part 5: Security Features

✅ **XSS Protection**: Tokens in HTTP-only cookies, not accessible by JavaScript

✅ **CSRF Protection**: SameSite=Lax cookies, plus CSRF token (if needed)

✅ **Secure Transport**: Cookies only sent over HTTPS in production

✅ **Token Expiration**: Access tokens expire in 24 hours, refresh tokens in 7 days

✅ **Token Rotation**: New tokens issued on each refresh

✅ **Session Verification**: Backend validates token on each request

✅ **Explicit Logout**: User sessions can be terminated immediately

---

## Part 6: Testing Checklist

- [ ] User logs in → Tokens in cookies (DevTools → Application → Cookies)
- [ ] User presses F5 on /tasks → Stays on /tasks (not redirected to login)
- [ ] User closes browser → Cookie persists across browser sessions
- [ ] User logs out → Cookies cleared
- [ ] User tries accessing /tasks without logging in → Redirected to /login
- [ ] Authenticated user tries accessing /login → Redirected to /tasks
- [ ] Token expires → Auto-refresh works silently
- [ ] User loads app with expired token → New token issued
- [ ] Multiple tabs open → All share same session
- [ ] API call fails with 401 → Automatically retries after refresh

---

## Summary

**Problem**: Refresh redirected authenticated users to login

**Root Cause**:
- Tokens stored in localStorage (not available on initial render)
- Race condition between component render and token loading
- No server-side session verification

**Solution**:
- Store tokens in HTTP-only cookies (secure, automatic transmission)
- Verify session on app load with `/api/auth/verify` endpoint
- Protect routes with `<ProtectedRoute>` wrapper
- No redirect happens when session is valid

**Result**:
- User stays logged in after refresh ✓
- Session persists across browser closures ✓
- Tokens auto-refresh when expired ✓
- Maximum security with cookies ✓

