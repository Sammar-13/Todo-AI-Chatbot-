# Authentication Persistence - Quick Reference Guide

## The Problem (In 30 Seconds)

```
User logs in → Works fine ✓
User presses F5 → Redirected to login ❌

Why? Tokens are in localStorage but not loaded on initial render.
This causes a race condition where the app redirects to login
before the token is found.
```

## The Solution (In 30 Seconds)

```
1. Store tokens in HTTP-only cookies (not localStorage)
2. Browser auto-sends cookies on every request
3. Backend verifies cookies on app load
4. Frontend stays on current page ✓
```

---

## Implementation Checklist

### Backend (FastAPI)

- [ ] Create `middleware/auth.py` with cookie verification
- [ ] Add `set_auth_cookies()` function to auth endpoints
- [ ] Update `/auth/register` to set cookies
- [ ] Update `/auth/login` to set cookies
- [ ] Update `/auth/refresh` to use refresh_token from cookie
- [ ] Add POST `/auth/logout` to clear cookies
- [ ] Add GET `/auth/verify` for session verification
- [ ] Update `dependencies.py` to check cookies instead of headers

### Frontend (Next.js)

- [ ] Update API client to use `credentials: "include"`
- [ ] Remove localStorage token management
- [ ] Rewrite `AuthContext.tsx` to verify session on app load
- [ ] Create `ProtectedRoute.tsx` component
- [ ] Wrap dashboard routes with `<ProtectedRoute requireAuth={true}>`
- [ ] Wrap login/signup routes with `<ProtectedRoute requireAuth={false}>`
- [ ] Update `(dashboard)/layout.tsx` to use ProtectedRoute
- [ ] Create `(auth)/layout.tsx` to guard login/signup pages

---

## Key Code Snippets

### Backend: Set Cookies

```python
def set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=86400,  # 24 hours
        httponly=True,
        secure=settings.is_production,
        samesite="lax",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=604800,  # 7 days
        httponly=True,
        secure=settings.is_production,
        samesite="lax",
    )
```

### Backend: Verify Session

```python
@router.get("/verify")
async def verify_session(request: Request, session: AsyncSession = Depends(get_session)):
    token = request.cookies.get("access_token")
    if not token:
        return {"authenticated": False}

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        user_id = UUID(payload.get("sub"))
        user = await session.get(User, user_id)
        return {"authenticated": True, "user": UserRead.model_validate(user)}
    except:
        return {"authenticated": False}
```

### Frontend: App Load Verification

```typescript
useEffect(() => {
  const initializeAuth = async () => {
    const response = await fetch('/api/auth/verify', {
      method: 'GET',
      credentials: 'include',  // Send cookies
    })
    const data = await response.json()

    if (data.authenticated) {
      setState({ isAuthenticated: true, user: data.user })
    } else {
      setState({ isAuthenticated: false })
    }
  }
  initializeAuth()
}, [])
```

### Frontend: Protected Route

```typescript
export function ProtectedRoute({ children, requireAuth = true }) {
  const { isAuthenticated, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (isLoading) return
    if (requireAuth && !isAuthenticated) router.push('/login')
    if (!requireAuth && isAuthenticated) router.push('/tasks')
  }, [isAuthenticated, isLoading])

  if (isLoading) return <LoadingSpinner />

  // Check again before rendering
  if (requireAuth && !isAuthenticated) return null
  if (!requireAuth && isAuthenticated) return null

  return <>{children}</>
}
```

---

## Before & After Comparison

### BEFORE (Current - Broken)

```
User logs in
  ↓
Tokens saved to localStorage
  ↓
User presses F5
  ↓
App renders with isAuthenticated = false (token not loaded yet)
  ↓
DashboardLayout redirects to /login
  ↓
After 100ms, token loads from localStorage
  ↓
BUT user already on login page ❌
```

### AFTER (Fixed)

```
User logs in
  ↓
Tokens set as HTTP-only cookies
  ↓
User presses F5
  ↓
App initializes AuthContext
  ↓
Calls /api/auth/verify with cookie
  ↓
Backend finds valid cookie
  ↓
Returns authenticated user
  ↓
AuthContext sets isAuthenticated = true
  ↓
User stays on current page ✓
```

---

## Testing Commands

### Check Cookies in Browser

```javascript
// Open DevTools Console and run:
document.cookie

// Should show:
// access_token=eyJhbGci...; refresh_token=eyJhbGci...
```

### Test Verify Endpoint

```bash
# After login, check if cookies are being sent
curl -i -b "access_token=YOUR_TOKEN" http://localhost:8000/api/auth/verify

# Should return 200 with user data
```

### Test Login Flow

```bash
# 1. Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}' \
  -c cookies.txt

# 2. Check cookies saved
cat cookies.txt

# 3. Use cookies in next request
curl -b cookies.txt http://localhost:8000/api/tasks
```

---

## Common Issues & Fixes

### Issue: Cookies Not Being Set

**Check**:
1. Response headers include `Set-Cookie` headers
2. Server is NOT in "secure" mode with HTTP (cookies require HTTPS in secure mode)
3. Frontend is using `credentials: "include"` in fetch

**Fix**: In development, set `secure=False` in cookies:
```python
secure=settings.is_production  # False in dev, True in prod
```

### Issue: Cookies Not Being Sent

**Check**: DevTools → Network → Request Headers include `Cookie:`

**Fix**: Ensure fetch has `credentials: "include"`:
```typescript
fetch(url, {
  credentials: "include",  // THIS IS REQUIRED
})
```

### Issue: User Still Redirects After Refresh

**Check**:
1. Is `isLoading` false before rendering dashboard?
2. Is ProtectedRoute checking `isLoading` state?

**Fix**: Add loading check:
```typescript
if (isLoading) return <LoadingSpinner />
// Don't render content until auth is verified
```

### Issue: CORS Error with Cookies

**Backend CORS config must include**:
```python
CORSMiddleware(
    app,
    allow_credentials=True,  # REQUIRED for cookies
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Security Best Practices

✅ **DO**:
- Use HTTP-only cookies for tokens
- Include `Secure` flag for HTTPS (production)
- Include `SameSite=Lax` for CSRF protection
- Verify token on server for every request
- Set short expiration (24 hours for access token)
- Use refresh token for long sessions

❌ **DON'T**:
- Store tokens in localStorage
- Store tokens in sessionStorage
- Send tokens in URL parameters
- Skip server-side verification
- Use long-lived access tokens
- Send tokens in unencrypted requests

---

## File Locations

**Backend Files to Create/Modify**:
- `backend/src/app/middleware/auth.py` (NEW)
- `backend/src/app/api/v1/auth.py` (MODIFY)
- `backend/src/app/api/dependencies.py` (MODIFY)
- `backend/src/app/main.py` (UPDATE CORS)

**Frontend Files to Create/Modify**:
- `frontend/src/utils/api.ts` (MODIFY)
- `frontend/src/context/AuthContext.tsx` (REWRITE)
- `frontend/src/components/ProtectedRoute.tsx` (NEW)
- `frontend/src/app/(dashboard)/layout.tsx` (MODIFY)
- `frontend/src/app/(auth)/layout.tsx` (NEW)

---

## Implementation Time Estimate

- Backend: 1-2 hours (cookie setup, middleware, endpoints)
- Frontend: 1-2 hours (API client, AuthContext, ProtectedRoute)
- Testing: 30-60 minutes
- **Total**: 3-5 hours for complete implementation

---

## Key Differences: Cookies vs localStorage

| Feature | Cookies | localStorage |
|---------|---------|--------------|
| **XSS Vulnerable** | No (HTTP-only) | Yes |
| **Auto-sent** | Yes | No (manual) |
| **CSRF Vulnerable** | Yes (need SameSite) | No |
| **Expiration** | Automatic | Manual |
| **Size Limit** | 4KB | 5-10MB |
| **Persistence** | Browser | Browser |
| **Domain** | Specific domain | Any domain |

---

## Next Steps

1. **Read**: Full `AUTH_PERSISTENCE_ANALYSIS.md` for complete details
2. **Implement**: Follow the code examples in correct order
3. **Test**: Use the testing checklist
4. **Debug**: Check console and network tabs if issues arise
5. **Verify**: Run through all test cases before deploying

---

**Status**: Ready for implementation
**Difficulty**: Medium
**Security**: High
**User Experience**: Excellent

