# Authentication Persistence - Implementation Summary

## Executive Summary

**Current Issue**: User logged in → Page refresh → User redirected to login (session lost)

**Solution**: Replace localStorage with HTTP-only cookies and server-side session verification

**Result**: User stays logged in after refresh, across browser sessions, and page navigations

**Implementation Effort**: 3-5 hours

**Security Level**: Production-ready

---

## Problem Analysis

### Root Cause

```
Timeline of Broken Flow:

1. Page Reloads
   ↓
2. React App Initializes
   ↓
3. Components Render (including DashboardLayout)
   ↓
4. DashboardLayout Checks: isAuthenticated = false (tokens not loaded yet)
   ↓
5. DashboardLayout Redirects to /login
   ↓
6. THEN useEffect runs and loads tokens from localStorage
   ↓
7. Too late - user already redirected ❌
```

**Why?**
- Tokens stored in localStorage
- localStorage not available during initial render
- React component renders before useEffect runs
- Race condition between component render and token loading

---

## Solution Overview

### HTTP-Only Cookies Approach

```
Browser Behavior:
┌─────────────────────────────────────────┐
│   HTTP-Only Cookie Set by Backend       │
│   ─────────────────────────────────     │
│   - Cannot be accessed by JavaScript    │
│   - Automatically sent on every request │
│   - Survives page refresh               │
│   - Survives browser close/reopen       │
└─────────────────────────────────────────┘

Backend Behavior:
┌─────────────────────────────────────────┐
│   /api/auth/verify Endpoint             │
│   ─────────────────────────────────     │
│   - Called on app load                  │
│   - Checks cookie                       │
│   - Validates JWT signature             │
│   - Returns user if valid               │
│   - No redirect happens                 │
└─────────────────────────────────────────┘

Frontend Behavior:
┌─────────────────────────────────────────┐
│   App Load → Verify Session             │
│   ─────────────────────────────────     │
│   - AuthProvider calls /verify          │
│   - Backend checks cookie               │
│   - Sets isAuthenticated = true/false   │
│   - No race condition                   │
│   - Correct state on first render       │
└─────────────────────────────────────────┘
```

---

## Implementation Steps

### Phase 1: Backend (2-3 hours)

#### Step 1: Create Auth Middleware
**File**: `backend/src/app/middleware/auth.py`

```python
async def verify_token_from_cookie(request: Request) -> Optional[dict]:
    """Extract and verify JWT from HTTP-only cookie"""
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        if payload.get("type") != "access":
            return None
        return payload
    except JWTError:
        return None
```

#### Step 2: Add Cookie Functions to Auth Routes
**File**: `backend/src/app/api/v1/auth.py`

```python
def set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    """Set HTTP-only cookies for authentication"""
    response.set_cookie("access_token", access_token, max_age=86400, httponly=True, secure=settings.is_production, samesite="lax")
    response.set_cookie("refresh_token", refresh_token, max_age=604800, httponly=True, secure=settings.is_production, samesite="lax")
```

**Update endpoints**:
- `@router.post("/register")` → Add `set_auth_cookies(response, access_token, refresh_token)`
- `@router.post("/login")` → Add `set_auth_cookies(response, access_token, refresh_token)`
- `@router.post("/refresh")` → Get token from `request.cookies.get("refresh_token")`
- `@router.post("/logout")` → Clear cookies with `response.delete_cookie()`

#### Step 3: Add Session Verification Endpoint
**File**: `backend/src/app/api/v1/auth.py`

```python
@router.get("/verify")
async def verify_session(request: Request, session: AsyncSession = Depends(get_session)):
    """Verify current session from cookie"""
    payload = await verify_token_from_cookie(request)
    if not payload:
        return {"authenticated": False}

    user_id = UUID(payload.get("sub"))
    user = await session.get(User, user_id)

    if not user:
        return {"authenticated": False}

    return {"authenticated": True, "user": UserRead.model_validate(user)}
```

#### Step 4: Update CORS Configuration
**File**: `backend/src/app/main.py`

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,  # CRITICAL for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Phase 2: Frontend (1-2 hours)

#### Step 1: Update API Client
**File**: `frontend/src/utils/api.ts`

```typescript
async fetchAPI<T>(endpoint: string, options: FetchOptions = {}): Promise<T> {
    const fetchOptions: RequestInit = {
        ...options,
        credentials: "include",  // CRITICAL: Send cookies
        headers: { 'Content-Type': 'application/json' },
    }

    const response = await fetch(url, fetchOptions)
    // ... error handling ...
}

// Remove manual token management (setToken, getAccessToken, etc)
```

#### Step 2: Rewrite AuthContext
**File**: `frontend/src/context/AuthContext.tsx`

```typescript
useEffect(() => {
    const initializeAuth = async () => {
        try {
            const response = await fetch('/api/auth/verify', {
                method: 'GET',
                credentials: 'include',  // Send cookies
            })
            const data = await response.json()

            if (data.authenticated && data.user) {
                setState({
                    user: data.user,
                    isAuthenticated: true,
                    isLoading: false,
                })
            } else {
                setState({
                    user: null,
                    isAuthenticated: false,
                    isLoading: false,
                })
            }
        } catch (error) {
            setState({ isLoading: false })
        }
    }

    initializeAuth()
}, [])
```

#### Step 3: Create Protected Route Component
**File**: `frontend/src/components/ProtectedRoute.tsx`

```typescript
export function ProtectedRoute({ children, requireAuth = true }) {
    const { isAuthenticated, isLoading } = useAuth()
    const router = useRouter()

    useEffect(() => {
        if (isLoading) return

        if (requireAuth && !isAuthenticated) {
            router.push('/login')
        } else if (!requireAuth && isAuthenticated) {
            router.push('/tasks')
        }
    }, [isAuthenticated, isLoading, requireAuth, router])

    if (isLoading) return <LoadingSpinner />

    if (requireAuth && !isAuthenticated) return null
    if (!requireAuth && isAuthenticated) return null

    return <>{children}</>
}
```

#### Step 4: Protect Routes
**File**: `frontend/src/app/(dashboard)/layout.tsx`

```typescript
return (
    <ProtectedRoute requireAuth={true}>
        <div className="min-h-screen bg-gray-50">
            {/* Dashboard content */}
        </div>
    </ProtectedRoute>
)
```

**File**: `frontend/src/app/(auth)/layout.tsx` (NEW)

```typescript
export default function AuthLayout({ children }) {
    return (
        <ProtectedRoute requireAuth={false}>
            {children}
        </ProtectedRoute>
    )
}
```

---

## New User Flows

### Login & Refresh Flow

```
1. User visits /login
2. Enters credentials
3. POST /api/auth/login
   ├─ Backend validates
   ├─ Returns tokens
   └─ Sets HTTP-only cookies ✓

4. Frontend receives response
5. Sets AuthContext (isAuthenticated = true)
6. Redirects to /tasks

7. User presses F5
8. App reinitializes
9. AuthProvider.useEffect calls GET /api/auth/verify
10. Browser auto-sends cookie ✓
11. Backend validates cookie
12. Returns {authenticated: true, user: {...}}
13. Frontend sets state (isAuthenticated = true)
14. User stays on /tasks ✓ (NO REDIRECT)
```

### Close & Reopen Browser

```
1. User logs in → Cookies set with 24h expiration
2. User closes browser completely
3. Opens new browser window 24 hours later
4. Goes to http://localhost:3000
5. App initializes → Calls GET /api/auth/verify
6. Cookie still valid (24h expiration) ✓
7. Backend returns authenticated user
8. User automatically logged in ✓
```

### Token Expiration & Refresh

```
1. Access token about to expire
2. User makes API call
3. Backend returns 401 Unauthorized
4. API client catches 401
5. Calls POST /api/auth/refresh
6. Browser sends refresh_token cookie ✓
7. Backend issues new access_token
8. Sets new HTTP-only cookie ✓
9. API client retries original request
10. Success ✓
```

---

## Security Features

### Token Storage

| Method | XSS Safe | Auto-sent | Persistence | Status |
|--------|----------|-----------|-------------|--------|
| localStorage | ❌ No | ❌ Manual | ✓ Yes | Current (unsafe) |
| HTTP-only Cookie | ✅ Yes | ✅ Auto | ✓ Yes | **Recommended** |

### Protection Mechanisms

- ✅ **HTTP-only flag**: JavaScript cannot access token
- ✅ **Secure flag**: HTTPS only (production)
- ✅ **SameSite=Lax**: CSRF protection
- ✅ **Short expiration**: Access token expires in 24 hours
- ✅ **Refresh token**: Long-lived (7 days)
- ✅ **Server validation**: Every request validated
- ✅ **Token rotation**: New tokens on each refresh

---

## Testing Checklist

### Manual Testing

- [ ] Login with credentials → See token in cookies
- [ ] Press F5 on /tasks → Stay on /tasks (no redirect)
- [ ] Close browser → Reopen → Still logged in (within 24h)
- [ ] Click logout → Cookies cleared
- [ ] Try accessing /tasks without login → Redirect to /login
- [ ] Logged in user visits /login → Redirect to /tasks
- [ ] Multiple tabs open → Share same session
- [ ] API fails with 401 → Auto-refresh → Retry succeeds

### Browser DevTools

```
1. Open DevTools (F12)
2. Go to Application → Cookies → localhost:3000
3. Should see:
   - access_token=eyJhbGci...
   - refresh_token=eyJhbGci...
   - Both with HttpOnly flag ✓
```

### Network Inspector

```
1. Open Network tab
2. Perform API request
3. Check Request Headers:
   - Should include: Cookie: access_token=...; refresh_token=...
4. Check Response Headers:
   - Login/refresh should include: Set-Cookie headers
```

---

## Rollout Plan

### Phase 1: Backend Implementation (Day 1)
- [ ] Create middleware/auth.py
- [ ] Update auth endpoints with set_auth_cookies()
- [ ] Add /verify endpoint
- [ ] Update CORS for credentials
- [ ] Test with curl/Postman

### Phase 2: Frontend Implementation (Day 1-2)
- [ ] Update API client for credentials: "include"
- [ ] Rewrite AuthContext for /verify
- [ ] Create ProtectedRoute component
- [ ] Wrap dashboard routes
- [ ] Wrap auth routes

### Phase 3: Testing (Day 2)
- [ ] Manual testing all flows
- [ ] Browser DevTools inspection
- [ ] Network tab verification
- [ ] Edge cases (expired tokens, multiple tabs, etc)

### Phase 4: Deployment (Day 3)
- [ ] Deploy backend with cookie endpoints
- [ ] Deploy frontend with new auth flow
- [ ] Monitor for issues
- [ ] User acceptance testing

---

## Troubleshooting

### Cookies Not Being Set

**Symptom**: No cookies in DevTools → Application → Cookies

**Causes**:
1. `secure=True` but using HTTP (not HTTPS)
2. `allow_credentials=False` in CORS
3. Missing `httponly=True` parameter

**Fix**:
```python
# Development
secure=settings.is_production  # False in dev

# Production
secure=True  # HTTPS required

# CORS
allow_credentials=True  # Must be True
```

### Cookies Not Being Sent

**Symptom**: Network tab shows no Cookie header

**Causes**:
1. Missing `credentials: "include"` in fetch
2. Cross-origin request without credentials
3. Cookie domain mismatch

**Fix**:
```typescript
fetch(url, {
    credentials: "include",  // REQUIRED
})
```

### Still Redirecting After Refresh

**Symptom**: User still goes to /login after F5

**Causes**:
1. ProtectedRoute rendering before auth check
2. `isLoading` not being checked
3. `/verify` endpoint not returning user

**Fix**: Ensure `isLoading` is checked before rendering:
```typescript
if (isLoading) return <LoadingSpinner />

if (requireAuth && !isAuthenticated) {
    router.push('/login')
    return null
}
```

---

## Files Summary

### Backend Files

| File | Change | Purpose |
|------|--------|---------|
| `middleware/auth.py` | NEW | Cookie verification |
| `api/v1/auth.py` | MODIFY | Set/clear cookies, add /verify |
| `api/dependencies.py` | MODIFY | Check cookies instead of headers |
| `main.py` | MODIFY | Update CORS for credentials |

### Frontend Files

| File | Change | Purpose |
|------|--------|---------|
| `utils/api.ts` | MODIFY | Add `credentials: "include"` |
| `context/AuthContext.tsx` | REWRITE | Call /verify on load |
| `components/ProtectedRoute.tsx` | NEW | Route protection |
| `app/(dashboard)/layout.tsx` | MODIFY | Use ProtectedRoute |
| `app/(auth)/layout.tsx` | NEW | Guard login/signup |

---

## Expected Outcomes

✅ **After Implementation**:
- User stays logged in after F5
- Session persists across browser close/reopen
- Tokens auto-refresh when expired
- Login/signup pages protected
- Dashboard routes protected
- Maximum security with cookies

✅ **User Experience**:
- Seamless session continuation
- No unexpected redirects
- Smooth token refresh
- Secure by default

✅ **Security**:
- Tokens not accessible via XSS
- CSRF protection with SameSite
- HTTPS enforcement in production
- Server-side validation on every request

---

## Success Criteria

- [ ] User login → Tokens in HTTP-only cookies
- [ ] User refresh → No redirect to /login
- [ ] User browser close/reopen → Still logged in (within 24h)
- [ ] User logout → Cookies cleared
- [ ] Token refresh → Automatic, no user interaction
- [ ] Unauthenticated user → Cannot access /tasks
- [ ] Authenticated user → Cannot access /login (redirects to /tasks)
- [ ] Network error → Graceful error handling
- [ ] All tests passing

---

## Timeline

| Phase | Duration | Tasks |
|-------|----------|-------|
| Planning | 1 hour | Review docs, plan implementation |
| Backend | 2 hours | Middleware, endpoints, CORS |
| Frontend | 2 hours | API client, AuthContext, routes |
| Testing | 1 hour | Manual testing, edge cases |
| **Total** | **6 hours** | |

---

## References

- Full Analysis: `AUTH_PERSISTENCE_ANALYSIS.md`
- Quick Reference: `AUTH_QUICK_REFERENCE.md`
- JWT Cookies: https://auth0.com/blog/cookies-vs-tokens-definitive-guide/
- HTTP-only Cookies: https://owasp.org/www-community/attacks/csrf
- Next.js Protected Routes: https://nextjs.org/docs/app/building-your-application/routing/route-groups

---

**Status**: Ready for Implementation
**Priority**: High
**Complexity**: Medium
**Impact**: Critical for UX

