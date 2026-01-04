# HTTP-Only Cookie Authentication - Quick Test Guide

**Status**: Ready for Testing
**Implementation Date**: January 3, 2026

---

## What Was Fixed

**Problem**: User logs in → Refresh page → Gets redirected to login ❌

**Solution**: Tokens now stored in HTTP-only cookies with server-side session verification ✅

---

## Quick Start Testing

### Step 1: Verify Backend is Running
```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --reload

# Should show: Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Verify Frontend is Running
```bash
# Terminal 2: Frontend
cd frontend
npm run dev

# Should show: ready - started server on 0.0.0.0:3000
```

### Step 3: Test Login
1. Go to http://localhost:3000
2. Click "Log In" (or Sign Up for new account)
3. Enter credentials
4. ✅ Should redirect to /tasks
5. ✅ Should see your tasks

---

## Critical Test: Page Refresh

### Test the Fix
```
1. You're on /tasks (logged in)
2. Press Ctrl+R (or Cmd+R) to refresh
3. EXPECTED: ✅ Stay on /tasks, still see tasks
4. OLD BUG: ❌ Would redirect to /login
```

**This is the main fix!**

---

## Essential Tests

### Test 1: Login Persistence
```
1. Log in to /tasks
2. Refresh page (F5, Ctrl+R, Cmd+R)
3. ✅ Still logged in, same page
```

### Test 2: Session After Browser Close
```
1. Log in
2. Close browser completely (all windows)
3. Open browser again
4. Go to http://localhost:3000
5. ✅ Should go to /tasks (auto-logged in)
```

### Test 3: Logout Works
```
1. Go to /tasks
2. Click logout button
3. ✅ Redirects to /login
```

### Test 4: Cookies Exist
```
1. Log in
2. DevTools (F12) → Application → Cookies
3. ✅ Should see:
   - access_token (HttpOnly: Yes)
   - refresh_token (HttpOnly: Yes)
```

### Test 5: Cannot Access Auth Pages When Logged In
```
1. Go to /tasks (logged in)
2. Try to visit http://localhost:3000/login
3. ✅ Redirects back to /tasks
```

### Test 6: Cannot Access Dashboard When Logged Out
```
1. Clear cookies (DevTools → delete all)
2. Go to http://localhost:3000/tasks
3. ✅ Redirects to /login
```

---

## Detailed Testing

### DevTools Verification

#### Check 1: Verify Cookies Are Set
```
1. Log in
2. Open DevTools (F12)
3. Go to Application → Cookies → localhost:3000
4. Look for:
   ✅ access_token
   ✅ refresh_token
5. Both should have HttpOnly = Yes
```

#### Check 2: Verify Cookies Auto-Sent
```
1. Log in
2. DevTools → Network tab
3. Go to /tasks or make any API call
4. Click on request (e.g., GET /api/tasks)
5. Click Headers tab
6. Look for "Cookie" in Request Headers
7. Should show: Cookie: access_token=xxx; refresh_token=xxx
```

#### Check 3: No Tokens in LocalStorage
```
1. DevTools → Application → Local Storage
2. Should be EMPTY (no access_token, no refresh_token)
3. Tokens ONLY in cookies, not in storage
```

---

## API Endpoints to Test

### Login/Register
```bash
# Test login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  -c cookies.txt

# Should return tokens in response + set cookies
```

### Verify Session (NEW)
```bash
# Test session verification
curl -X GET http://localhost:8000/api/auth/verify \
  -b cookies.txt

# Should return: {"authenticated": true, "user": {...}}
```

### Refresh Token
```bash
# Test token refresh
curl -X POST http://localhost:8000/api/auth/refresh \
  -b cookies.txt

# Should return new tokens + set new cookies
```

### Logout
```bash
# Test logout
curl -X POST http://localhost:8000/api/auth/logout \
  -b cookies.txt

# Should clear cookies and return success message
```

---

## Common Issues & Fixes

### Issue: Still Redirected to Login After Refresh
**Solution**:
1. Check browser console for errors (F12)
2. Check network tab - is GET /api/auth/verify called?
3. Check if /verify endpoint returns correct response
4. Make sure cookies exist and are valid

### Issue: Cookies Not Appearing in DevTools
**Solution**:
1. Make sure login was successful (no errors)
2. Check network response headers for Set-Cookie
3. Check if cookies are set on correct domain (localhost)
4. Try in incognito/private window (might clear cookies)

### Issue: Cookies Showing But Not Sent in Requests
**Solution**:
1. Check if API client has `credentials: 'include'`
2. Check CORS header: `allow_credentials=True`
3. Check request headers have Cookie field
4. Make sure not using different domain

### Issue: "Cannot find LoadingSpinner component"
**Solution**:
1. Check if `LoadingSpinner` exists
2. Check import path in ProtectedRoute
3. If missing, create simple spinner component

---

## Expected Behavior Timeline

### Scenario 1: Fresh Login
```
0s:   User at /login
1s:   User enters credentials, clicks "Log In"
2s:   POST /auth/login → Success
      Backend sets cookies (Set-Cookie headers)
      Response includes user data
3s:   Frontend receives response
      Sets AuthContext: isAuthenticated=true
      Shows loading spinner briefly
4s:   AuthProvider initializes (app load)
      Calls GET /auth/verify
      Receives authenticated: true
      Renders protected content
5s:   User redirects to /tasks
6s:   ✅ Tasks page displayed
      Cookies visible in DevTools
```

### Scenario 2: Page Refresh
```
0s:   User on /tasks (logged in)
1s:   User presses F5
      Page starts reloading
2s:   App reinitializes
      AuthProvider.useEffect runs
3s:   Calls GET /api/auth/verify
      Browser auto-sends access_token cookie
4s:   Backend validates token
      Returns authenticated: true, user: {...}
5s:   AuthContext sets state
      ProtectedRoute checks: authenticated=true
6s:   Renders dashboard content
7s:   ✅ User STAYS on /tasks
      No redirect happened
```

### Scenario 3: Token Expiration
```
... Time passes (24 hours for access token) ...

1s:   User makes API request
2s:   Backend returns 401 Unauthorized
3s:   API client catches 401
4s:   Calls POST /api/auth/refresh
      Browser sends refresh_token cookie
5s:   Backend creates new access_token
      Sets new cookie
6s:   API client retries original request
7s:   ✅ Original request succeeds
      User doesn't notice anything
```

---

## Manual Testing Checklist

### Before Testing
- [ ] Backend is running (port 8000)
- [ ] Frontend is running (port 3000)
- [ ] Database is connected
- [ ] Test user account exists or can be created

### Core Functionality Tests
- [ ] Login works
- [ ] Redirect to /tasks after login
- [ ] Tasks display correctly
- [ ] Logout works and redirects to /login
- [ ] Cannot access /tasks without login

### Persistence Tests (THE MAIN FIX)
- [ ] Page refresh (F5) - stays logged in ✅
- [ ] Close browser and reopen - still logged in ✅
- [ ] Multiple tabs - session shared ✅
- [ ] Different routes - stay logged in ✅

### Cookie Tests
- [ ] Cookies exist in DevTools
- [ ] Cookies have HttpOnly flag
- [ ] Cookies auto-sent in requests
- [ ] No tokens in localStorage
- [ ] Cookies cleared on logout

### Security Tests
- [ ] Cannot view token value in JavaScript
- [ ] Cannot access protected routes without auth
- [ ] Cannot access login page when already logged in
- [ ] Token refresh works on 401
- [ ] CORS allows cookies

### Edge Cases
- [ ] Network error handling
- [ ] API timeout handling
- [ ] Invalid credentials rejection
- [ ] User deletion/deactivation
- [ ] Session conflicts (multiple logins)

---

## Success Indicators

### ✅ You Know It's Working When:

1. **After page refresh, you're still logged in** ← MAIN FIX
2. Cookies appear in DevTools with HttpOnly flag
3. Closing/reopening browser keeps you logged in (within 7 days)
4. Logout actually clears cookies
5. Login/signup pages redirect to /tasks when already logged in
6. Cannot access /tasks without valid session
7. Network tab shows cookies being sent automatically
8. No tokens appear in localStorage
9. Token refresh happens automatically on 401
10. Multiple tabs share same session

---

## Performance Notes

### Expected Response Times
- Login: < 500ms
- Session verify: < 100ms
- Task API calls: < 200ms
- Logout: < 100ms

### Expected Behavior
- No visible flicker when refresh checking auth
- LoadingSpinner shows briefly while checking
- Auto-redirect happens smoothly
- No 401 errors should appear to user (auto-refresh)

---

## Rollback Instructions (If Needed)

If you need to go back to localStorage:

1. Restore from git history
2. Changes are in these files:
   - backend: `api/v1/auth.py`, `middleware/auth.py`
   - frontend: `utils/api.ts`, `context/AuthContext.tsx`, `components/ProtectedRoute.tsx`

---

## Next Steps After Testing

### If All Tests Pass ✅
1. **Commit changes**
   ```bash
   git add .
   git commit -m "Implement HTTP-only cookie authentication (Task 02-050)"
   ```

2. **Test on staging environment** (if available)

3. **Deploy to production**

4. **Monitor login/logout events**

5. **Gather user feedback**

### If Tests Fail ❌
1. Check error logs in browser console (F12)
2. Check server logs (backend terminal)
3. Check network requests in DevTools
4. Review corresponding implementation section above
5. Create fix, test again

---

## Support

### For Questions:
- Check implementation details in `HTTP_ONLY_COOKIES_IMPLEMENTATION.md`
- Check earlier analysis documents
- Review auth endpoint code in `backend/src/app/api/v1/auth.py`
- Check frontend code in `frontend/src/context/AuthContext.tsx`

### Common Commands:
```bash
# Clear browser cookies (DevTools)
Right-click → Delete → All

# Restart backend
Ctrl+C, then: python -m uvicorn app.main:app --reload

# Restart frontend
Ctrl+C, then: npm run dev

# View backend logs
Check terminal output

# View frontend logs
Check browser console (F12)
```

---

**Status**: ✅ Ready for Testing
**Last Updated**: January 3, 2026
**Maintainer**: Implementation Team
