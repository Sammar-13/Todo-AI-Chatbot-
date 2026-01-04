# Manual Testing Guide - Step by Step with Screenshots

**URL**: http://localhost:3000
**Backend**: http://localhost:8000 (running ✅)
**Database**: SQLite (test.db)

---

## STEP 1️⃣: SIGNUP

### Open http://localhost:3000
You should see landing page with "Sign Up" and "Log In" buttons.

### Click "Sign Up" Button
Form appears with fields:
- Email
- Password
- Full Name

### Fill Form:
```
Email:     test@example.com
Password:  Test123!
Full Name: Test User
```

### Click "Sign Up"
```
EXPECT:
✅ Form submits (no error)
✅ Redirects to /tasks page
✅ Top right shows "Test User"
✅ Empty task list (no tasks created yet)
✅ Cookies set in browser
```

---

## STEP 2️⃣: VERIFY COOKIES SET

### Open DevTools (F12)

### Go to: Application → Cookies → localhost:3000

### Should see TWO cookies:
```
Name: access_token
Value: eyJhbGciOiJIUzI1NiIs... (long JWT)
HttpOnly: ✅ (checked)
Secure: false (in dev, true in prod)
SameSite: Lax
Path: /
Max-Age: 86400 (24 hours)

Name: refresh_token
Value: eyJhbGciOiJIUzI1NiIs... (long JWT)
HttpOnly: ✅ (checked)
Secure: false (in dev, true in prod)
SameSite: Lax
Path: /
Max-Age: 604800 (7 days)
```

### Verify LocalStorage is EMPTY:
```
Application → Local Storage → localhost:3000
Should be: EMPTY (no access_token or refresh_token keys)
```

---

## STEP 3️⃣: CREATE FIRST TASK

### On /tasks page, look for "Add Task" button or input field

### Enter task title:
```
"Buy groceries"
```

### Click "Create" or press Enter

### EXPECT:
```
✅ No error appears
✅ Task appears in list immediately
✅ Shows "Buy groceries" with status (pending)
✅ Task has all details
```

### Verify in Network Tab (DevTools):
```
DevTools → Network Tab
Look for: POST /api/tasks

Click it:
Status: 201 Created ✅
Response shows:
{
  "id": "xxx",
  "title": "Buy groceries",
  "status": "pending",
  "priority": "medium",
  "user_id": "xxx",
  "created_at": "2025-01-03..."
}

Request Headers show:
Cookie: access_token=...; refresh_token=...
```

---

## STEP 4️⃣: PAGE REFRESH (MAIN TEST!) ⭐⭐⭐

### YOU ARE ON /tasks page with task visible

### Press F5 (or Ctrl+R to refresh page)

### CRITICAL EXPECTATION:
```
✅ Page refreshes
✅ STAYS on /tasks page
✅ Does NOT redirect to /login
✅ Task still visible
✅ "Test User" still shows in top right
✅ NO login/signup page shown

❌ IF REDIRECT TO /login - TEST FAILED
```

### What Happens Behind The Scenes:
```
1. Page reload starts
2. App initializes
3. AuthProvider calls GET /api/auth/verify
4. Browser auto-sends access_token cookie
5. Backend verifies token
6. Returns {"authenticated": true, "user": {...}}
7. AuthContext sets state BEFORE first render
8. Component renders /tasks directly ✅
```

### Verify in Network Tab:
```
DevTools → Network Tab
Look for: GET /api/auth/verify

Click it:
Status: 200 OK ✅
Response: {"authenticated": true, "user": {...}} ✅
```

---

## STEP 5️⃣: CREATE SECOND TASK

### Still on /tasks page (after refresh)

### Create another task:
```
Title: "Pay bills"
```

### EXPECT:
```
✅ Task appears in list
✅ Now see TWO tasks:
   1. Buy groceries
   2. Pay bills
✅ User stayed logged in during all operations
```

---

## STEP 6️⃣: LOGOUT

### Find "Logout" button (usually in top navigation)

### Click "Logout"

### EXPECT:
```
✅ Redirects to /login page (or home page)
✅ NOT on /tasks anymore
✅ User not logged in
```

### Verify Cookies Cleared:
```
DevTools → Application → Cookies
SHOULD BE EMPTY:
❌ No access_token
❌ No refresh_token
```

---

## STEP 7️⃣: CLOSE BROWSER / NEW TAB

### Close browser completely OR open new incognito window

### Navigate to: http://localhost:3000

### EXPECT:
```
✅ See landing page / login page
✅ NOT automatically logged in
✅ NOT on /tasks
```

---

## STEP 8️⃣: LOGIN AGAIN

### On login page

### Fill form:
```
Email:    test@example.com
Password: Test123!
```

### Click "Log In"

### EXPECT:
```
✅ Redirects to /tasks
✅ Shows "Test User" in top right
✅ SEES BOTH PREVIOUSLY CREATED TASKS:
   1. Buy groceries ✅
   2. Pay bills ✅
✅ Tasks loaded from DATABASE (not browser)
```

### Verify Tasks in Network Tab:
```
DevTools → Network Tab
Look for: GET /api/tasks

Response should show:
[
  {
    "id": "xxx",
    "title": "Buy groceries",
    "status": "pending"
  },
  {
    "id": "xxx",
    "title": "Pay bills",
    "status": "pending"
  }
]

This proves tasks are in the database! ✅
```

---

## STEP 9️⃣: FINAL PAGE REFRESH

### On /tasks with both tasks visible

### Press F5 to refresh

### EXPECT:
```
✅ STAYS on /tasks (not redirected)
✅ Both tasks still visible
✅ User still logged in
✅ This proves session persistence works! ✅
```

---

## ✅ SUCCESS CHECKLIST

Mark each as complete:

### Authentication
- [ ] Signup creates account
- [ ] User redirects to /tasks
- [ ] Cookies set with HttpOnly flag
- [ ] Login works
- [ ] Logout works
- [ ] Logout clears cookies

### Session Persistence (MAIN FIX)
- [ ] After F5, stays on /tasks (NOT redirected to login) ⭐
- [ ] After F5, user still logged in ⭐
- [ ] After F5, user data visible ⭐
- [ ] /verify endpoint called on refresh ⭐

### Task Creation
- [ ] Can create task
- [ ] Task appears in list
- [ ] Task visible in network response
- [ ] Can create multiple tasks
- [ ] Can create task after page refresh

### Database Persistence
- [ ] Tasks visible after page refresh
- [ ] Tasks visible after logout/login
- [ ] Previous tasks still exist after login
- [ ] All task data persists

### Complete User Journey
- [ ] Signup → Create task → Refresh → Stays logged in ✅
- [ ] Logout → Login → See previously created tasks ✅
- [ ] Tasks persist across sessions ✅

---

## 🎯 THE MAIN TEST (Page Refresh)

**This is the critical test that proves the fix works:**

```
BEFORE FIX (Broken):
User on /tasks → Press F5 → Redirected to /login ❌

AFTER FIX (Working):
User on /tasks → Press F5 → STAYS on /tasks ✅
```

**If page refresh redirects to login, the fix didn't work.**

---

## 🔍 DEBUGGING - IF SOMETHING FAILS

### If redirect to login on F5:
```
1. Open DevTools Console (F12)
2. Look for error messages
3. Check Network tab for failed requests
4. Look for GET /api/auth/verify - did it succeed?
5. What was the response?
```

### If task doesn't appear:
```
1. Check Network tab: POST /api/tasks
2. Did it return 201 (success)?
3. Check Console for errors
4. Check backend logs
```

### If logout doesn't work:
```
1. Check Network tab: POST /auth/logout
2. Check Response headers: Set-Cookie headers?
3. Check Cookies after logout: Are they gone?
```

### If tasks don't appear after login:
```
1. Check Network tab: GET /api/tasks
2. Does it return task list?
3. Check response data
4. Check Console for errors
```

---

## 📱 EXPECTED APPEARANCE

### Landing Page (Before Login)
```
┌────────────────────────────────────┐
│  📝 Todo App                        │
│              [Sign Up] [Log In]     │
├────────────────────────────────────┤
│                                    │
│  Organize Your Tasks               │
│  Manage Your Life                  │
│                                    │
│  [Get Started Free]  [Sign In]    │
│                                    │
└────────────────────────────────────┘
```

### /tasks Page (After Login)
```
┌────────────────────────────────────┐
│  📝 Todo App    Test User [Logout]  │
├────────────────────────────────────┤
│ ☰ Sidebar  │  Add Task              │
│            │                        │
│            │  📌 Buy groceries      │
│            │     pending            │
│            │                        │
│            │  📌 Pay bills          │
│            │     pending            │
│            │                        │
└────────────────────────────────────┘
```

---

## ⏱️ ESTIMATED TIME

- Signup: 1 min
- Create task: 1 min
- Verify cookies: 1 min
- Page refresh: 1 min ⭐
- Create 2nd task: 1 min
- Logout: 1 min
- Login again: 1 min
- Verify tasks: 1 min
- Final refresh: 1 min

**Total: ~10 minutes**

---

## 🎉 WHEN DONE

All steps complete and passing:
```
✅ Signup works
✅ Task creation works
✅ Page refresh keeps user logged in (MAIN FIX)
✅ Tasks persist in database
✅ Logout works
✅ Login shows previous tasks
✅ Authentication is secure (HTTP-only cookies)
✅ Session persists across page refreshes
✅ Complete user journey works end-to-end
```

**You are done! The HTTP-only cookie authentication is working! 🚀**

---

**Status**: Ready for Manual Testing
**Time Estimate**: 10 minutes
**Success Criteria**: All 9 steps complete without errors
