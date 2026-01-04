# Complete End-to-End Testing Script

**Date**: January 3, 2026
**Status**: Ready for Manual Execution

---

## Test Scenario: Full User Journey

### Prerequisites
- Backend running on http://localhost:8000 ✅
- Frontend running on http://localhost:3000 ✅
- Browser DevTools ready (F12)

---

## Test Steps

### STEP 1: Signup
```
1. Open http://localhost:3000
2. Click "Sign Up"
3. Fill form:
   Email: test@example.com
   Password: Test123!
   Full Name: Test User
4. Click "Sign Up"

EXPECTED:
✅ Redirects to /tasks page
✅ Shows "Test User" in top navigation
✅ Empty task list (no tasks yet)
```

**Verify Cookies After Signup**:
```
DevTools (F12) → Application → Cookies
Should see:
✅ access_token (JWT)
✅ refresh_token (JWT)
✅ Both have HttpOnly: Yes
```

---

### STEP 2: Create Task
```
1. On /tasks page (logged in)
2. Look for "Add Task" button or input field
3. Click and enter task title: "Buy groceries"
4. Click "Create" or press Enter

EXPECTED:
✅ Task appears in the task list
✅ Task shows title "Buy groceries"
✅ No errors in console (F12 → Console)
```

**Verify in Network Tab**:
```
DevTools → Network Tab
Look for: POST /api/tasks
Status should be: 201 Created
Request Headers should include:
✅ Cookie: access_token=...; refresh_token=...
```

---

### STEP 3: Verify Database Storage
```
Check that task is stored in database:

1. Open DevTools → Network Tab
2. Go to /tasks or create another task
3. Look for GET /api/tasks request
4. Click it → Response
5. Should show: [{"id":"...", "title":"Buy groceries", ...}]

EXPECTED:
✅ Task data returned from backend
✅ Task has all fields (id, title, status, etc.)
✅ Confirms data is saved to SQLite database
```

---

### STEP 4: Page Refresh (MAIN TEST!)
```
1. On /tasks page (task visible, user logged in)
2. Press F5 (or Ctrl+R to refresh)

EXPECTED - THIS IS THE CRITICAL TEST:
✅ Page refreshes WITHOUT redirecting to /login
✅ Still on /tasks page after refresh
✅ Task is still visible
✅ User name still shows in top right
✅ NO login/signup page appears

WHAT HAPPENS BEHIND THE SCENES:
1. Page reloads
2. App calls GET /api/auth/verify
3. Browser sends access_token cookie automatically
4. Backend verifies token and returns user
5. AuthContext sets isAuthenticated=true BEFORE render
6. Page renders /tasks directly ✅

OLD BEHAVIOR (BEFORE FIX):
❌ Would redirect to /login
❌ User loses session
❌ Has to log in again
```

**Verify Network Request**:
```
DevTools → Network Tab → After F5
Look for: GET /api/auth/verify
Status: 200
Response should be: {"authenticated": true, "user": {...}}
```

---

### STEP 5: Create Second Task
```
1. Still on /tasks (after refresh)
2. Create another task: "Pay bills"
3. Verify both tasks visible:
   - Buy groceries
   - Pay bills

EXPECTED:
✅ Both tasks appear in list
✅ Both persisted to database
✅ User stayed logged in after F5
```

---

### STEP 6: Logout
```
1. Click "Logout" button (usually in Navigation/top-right)
2. Should redirect to /login or / page

EXPECTED:
✅ Redirects to login page
✅ Cookies cleared (check DevTools → Cookies)
✅ Cannot access /tasks without re-logging in
```

**Verify Cookies Cleared**:
```
DevTools → Application → Cookies → localhost:3000
Should see:
✅ access_token cookie GONE
✅ refresh_token cookie GONE
```

---

### STEP 7: Restart Application
```
1. Backend: Keep running (no restart needed)
2. Frontend: Close browser or navigate to different site
3. Wait 5 seconds
4. Open http://localhost:3000 in new browser window/tab

EXPECTED:
✅ See login page (not authenticated)
✅ Can see "Log In" and "Sign Up" buttons
✅ No user data visible
```

---

### STEP 8: Login with Previous Account
```
1. On login page
2. Click "Log In"
3. Fill form:
   Email: test@example.com
   Password: Test123!
4. Click "Log In"

EXPECTED:
✅ Redirects to /tasks page
✅ Shows "Test User" again
✅ Sees both previously created tasks:
   - Buy groceries
   - Pay bills
✅ Tasks loaded from database!
```

**Verify Tasks are from Database**:
```
The tasks visible are NOT from browser storage, but from:
1. Backend database (SQLite test.db)
2. User account stored with ID
3. Tasks queried from database via GET /api/tasks
4. Shows persistence works! ✅
```

---

### STEP 9: Page Refresh Again
```
1. On /tasks with previously saved tasks
2. Press F5 to refresh
3. Tasks should still be visible

EXPECTED:
✅ STAYS on /tasks (not redirected)
✅ Tasks still visible (same as before refresh)
✅ This proves session persistence works! ✅
```

---

## Success Criteria Checklist

### Authentication
- [ ] Signup creates account
- [ ] Cookies set after signup (HttpOnly flags)
- [ ] Login works with correct credentials
- [ ] Logout clears cookies
- [ ] Cannot access /tasks without login

### Session Persistence (MAIN FIX)
- [ ] After F5 refresh, stays on /tasks
- [ ] After F5 refresh, user still logged in
- [ ] After F5 refresh, user data visible
- [ ] Does NOT redirect to /login after refresh
- [ ] /verify endpoint called on app load

### Task Creation
- [ ] Can create task on /tasks
- [ ] Task appears in list immediately
- [ ] Task saved to database
- [ ] Can create multiple tasks

### Database Persistence
- [ ] Tasks visible after page refresh
- [ ] Tasks visible after logout/login
- [ ] Tasks visible after app restart
- [ ] Previous tasks still exist
- [ ] New tasks created

### Complete Flow
- [ ] Signup → Create task → Refresh → stays logged in ✅
- [ ] Logout → Login → See saved tasks ✅
- [ ] App restart → Login → See previous tasks ✅
- [ ] Multiple refreshes → User stays logged in ✅

---

## Expected Results Summary

### Test Result: PASS ✅
**If ALL steps work as expected:**
- Session persistence issue is FIXED
- Users stay logged in after page refresh
- Tasks persist in database
- Authentication works correctly
- HTTP-only cookies are secure

### Test Result: FAIL ❌
**If any step fails, check:**
1. Browser console (F12) for errors
2. Network tab for failed requests
3. Backend logs for API errors
4. DevTools cookies to verify they exist

---

## Detailed Network Requests to Verify

### Request 1: POST /auth/register (Signup)
```
Method: POST
URL: http://localhost:8000/api/auth/register
Body: {
  "email": "test@example.com",
  "password": "Test123!",
  "full_name": "Test User"
}

Response (201):
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "user": {
    "id": "123e...",
    "email": "test@example.com",
    "full_name": "Test User"
  }
}

Response Headers - CRITICAL:
Set-Cookie: access_token=...; Path=/; HttpOnly; SameSite=Lax
Set-Cookie: refresh_token=...; Path=/; HttpOnly; SameSite=Lax
```

### Request 2: POST /api/tasks (Create Task)
```
Method: POST
URL: http://localhost:8000/api/tasks
Headers:
  Cookie: access_token=...; refresh_token=...

Body: {
  "title": "Buy groceries",
  "priority": "medium"
}

Response (201):
{
  "id": "task-123",
  "title": "Buy groceries",
  "status": "pending",
  "priority": "medium",
  "user_id": "user-123",
  "created_at": "2025-01-03T..."
}
```

### Request 3: GET /api/auth/verify (Page Refresh)
```
Method: GET
URL: http://localhost:8000/api/auth/verify
Headers:
  Cookie: access_token=...; refresh_token=...

Response (200):
{
  "authenticated": true,
  "user": {
    "id": "123e...",
    "email": "test@example.com",
    "full_name": "Test User"
  }
}

THIS IS THE KEY REQUEST THAT KEEPS USER LOGGED IN AFTER REFRESH!
```

### Request 4: GET /api/tasks (After Refresh)
```
Method: GET
URL: http://localhost:8000/api/tasks
Headers:
  Cookie: access_token=...; refresh_token=...

Response (200):
{
  "tasks": [
    {
      "id": "task-123",
      "title": "Buy groceries",
      "status": "pending"
    },
    {
      "id": "task-124",
      "title": "Pay bills",
      "status": "pending"
    }
  ]
}
```

### Request 5: POST /auth/logout (Logout)
```
Method: POST
URL: http://localhost:8000/api/auth/logout
Headers:
  Cookie: access_token=...; refresh_token=...

Response (200):
{
  "message": "Successfully logged out"
}

Response Headers - IMPORTANT:
Set-Cookie: access_token=; Path=/; HttpOnly; Max-Age=0
Set-Cookie: refresh_token=; Path=/; HttpOnly; Max-Age=0
(Cookies deleted by setting Max-Age=0)
```

---

## Browser Console Output Expected

### After Signup
```
[No errors should appear]
GET http://localhost:3000/tasks 200
POST http://localhost:8000/api/auth/register 201
```

### After Task Creation
```
[No errors should appear]
POST http://localhost:8000/api/tasks 201
GET http://localhost:8000/api/tasks 200
```

### After Page Refresh (F5)
```
[No errors should appear]
GET http://localhost:8000/api/auth/verify 200
GET http://localhost:8000/api/tasks 200
[Page renders successfully]
```

### If Errors Appear
```
❌ Error: Failed to fetch
  → Check if backend is running
  → Check if URL is correct

❌ 401 Unauthorized
  → Token expired or invalid
  → Check /verify endpoint response

❌ 404 Not Found
  → Endpoint doesn't exist
  → Check backend routing

❌ CORS Error
  → Backend CORS not configured
  → Check allow_credentials=True
```

---

## Timeline

| Step | Time | Action |
|------|------|--------|
| 1 | 1 min | Signup |
| 2 | 1 min | Verify cookies |
| 3 | 1 min | Create first task |
| 4 | 1 min | Verify in network tab |
| 5 | 1 min | Page refresh (F5) |
| 6 | 1 min | Create second task |
| 7 | 1 min | Logout |
| 8 | 1 min | App restart |
| 9 | 1 min | Login again |
| 10 | 1 min | Verify previous tasks |
| 11 | 1 min | Final refresh |

**Total Time**: ~15 minutes

---

## Documentation

### Files Changed
- ✅ `backend/middleware/auth.py` - Cookie verification
- ✅ `backend/api/v1/auth.py` - Cookie handling + /verify endpoint
- ✅ `frontend/utils/api.ts` - credentials: include
- ✅ `frontend/context/AuthContext.tsx` - /verify on app load
- ✅ `frontend/app/(dashboard)/layout.tsx` - Protected
- ✅ `frontend/app/(auth)/layout.tsx` - Protected

### Key Features
- ✅ HTTP-only cookies (secure)
- ✅ Auto session verification
- ✅ Page refresh persistence
- ✅ Database storage
- ✅ Task persistence

---

## After Testing

If all tests pass:
1. ✅ Document results in TESTING_RESULTS.md
2. ✅ Verify no console errors
3. ✅ Check all cookies are HttpOnly
4. ✅ Confirm tasks in database
5. ✅ Ready for production!

---

**Status**: Ready for Manual Testing
**Expected Result**: ALL TESTS PASS ✅
**Main Fix Verification**: Page refresh stays on /tasks ✅
