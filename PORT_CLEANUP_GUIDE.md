# Port Cleanup & Configuration Guide

**Date**: January 1, 2026
**Issue**: Multiple processes running on ports 3000, 3001-3005, and 8000
**Solution**: Manual cleanup and proper configuration

---

## Current Status

### Ports in Use
```
Port 3000: PID 10632 (Next.js frontend)
Port 8000: Multiple Python processes (4 instances)
Ports 3001-3005: Previous dev server attempts
```

### Issue
- Port 3000 occupied by old dev server
- Port 8000 occupied by multiple backend instances
- Frontend keeps trying ports 3001-3005 since 3000 is taken
- Cannot start fresh servers on correct ports

---

## Solution: Manual Cleanup

### Option 1: Using Windows Task Manager (Easiest)

**Step 1**: Open Task Manager
- Press: `Ctrl + Shift + Esc` OR
- Press: `Ctrl + Alt + Delete` → Select "Task Manager"

**Step 2**: Find Node.js processes
- Look for: `node.exe` in the list
- Select each one and click "End Task"
- Confirm if prompted

**Step 3**: Find Python processes
- Look for: `python.exe` or `py.exe` in the list
- Select each one and click "End Task"
- Confirm if prompted

**Step 4**: Close the Task Manager
- All server processes should be stopped

---

### Option 2: Using Command Line (Manual)

**Step 1**: Open Command Prompt as Administrator
- Right-click on Command Prompt
- Select "Run as Administrator"

**Step 2**: Kill processes by name
```bash
# Kill all Node.js processes
taskkill /IM node.exe /F

# Kill all Python processes
taskkill /IM python.exe /F
taskkill /IM py.exe /F
```

**Step 3**: Verify ports are free
```bash
netstat -ano | find ":3000"
netstat -ano | find ":8000"
```
Should return nothing if ports are free.

---

### Option 3: Kill Specific PIDs (If you know them)

```bash
# Replace XXXX with the actual PID
taskkill /PID 10632 /F
taskkill /PID 3132 /F
taskkill /PID 6216 /F
taskkill /PID 4760 /F
taskkill /PID 5944 /F
taskkill /PID 7760 /F
```

---

## After Cleanup: Starting Servers Correctly

### Backend: Port 8000

**Step 1**: Open Command Prompt
```bash
cd "F:\GIAIC HACKATHONS\FULL STACK WEB APP\hackathon-todo\backend"
```

**Step 2**: Start the backend server
```bash
python -m uvicorn src.app.main:app --reload --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Keep this terminal open** (don't close it)

---

### Frontend: Port 3000

**Step 1**: Open NEW Command Prompt (don't close the backend one)
```bash
cd "F:\GIAIC HACKATHONS\FULL STACK WEB APP\hackathon-todo\frontend"
```

**Step 2**: Start the frontend development server
```bash
npm run dev -- --port 3000
```

**Expected Output**:
```
  ▲ Next.js 14.2.35
  - Local:        http://localhost:3000
  ✓ Starting...
```

---

## Verifying Everything is Running

### Test Backend
Open a new Command Prompt and run:
```bash
curl http://localhost:8000/health
```

Should return:
```json
{"status":"healthy"}
```

### Test Frontend
Open your browser and go to:
```
http://localhost:3000
```

Should see the Todo App home page (no 404 error)

---

## Port Configuration Summary

| Service | Port | Status | Command |
|---------|------|--------|---------|
| Backend | 8000 | Should be running | `python -m uvicorn src.app.main:app --reload --port 8000` |
| Frontend | 3000 | Should be running | `npm run dev -- --port 3000` |

---

## Configuration Files

### Frontend Port Configuration

If you need to permanently set port 3000, edit:

**File**: `frontend/next.config.js`

Add or modify:
```javascript
module.exports = {
  // ... other config ...
  env: {
    PORT: '3000',
  },
}
```

Or use environment variable:
```bash
PORT=3000 npm run dev
```

### Backend Port Configuration

The backend port is already set in the startup command:
```bash
python -m uvicorn src.app.main:app --reload --port 8000
```

To change port, modify the `--port` parameter.

---

## Environment Variables

### Create `.env.local` for Frontend

**File**: `frontend/.env.local`

```
# API endpoint (where backend is running)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Frontend port (optional, can also use command line)
PORT=3000
```

### Create `.env` for Backend

**File**: `backend/.env`

```
# Database connection
DATABASE_URL=postgresql://user:password@host/dbname

# JWT Secret
JWT_SECRET=your-secret-key

# Environment
DEBUG=True

# API Port (optional)
PORT=8000
```

---

## Troubleshooting

### Issue: "Address already in use"

**Solution 1**: Kill processes
```bash
taskkill /IM node.exe /F
taskkill /IM python.exe /F
```

**Solution 2**: Use different ports
```bash
# Frontend on different port
npm run dev -- --port 3001

# Backend on different port
python -m uvicorn src.app.main:app --reload --port 8001
```

**Solution 3**: Check what's using the port
```bash
netstat -ano | find ":3000"
# Get the PID from the output, then:
taskkill /PID XXXX /F
```

### Issue: Frontend can't connect to backend

**Solution**: Check `NEXT_PUBLIC_API_URL` in `.env.local`
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Make sure backend is running on port 8000.

### Issue: CORS errors

**Backend**: Ensure CORS is configured correctly in `src/app/main.py`
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Clean Start Checklist

- [ ] All Node.js processes killed
- [ ] All Python processes killed
- [ ] Ports 3000 and 8000 are free
- [ ] Backend terminal open, running on 8000
- [ ] Frontend terminal open, running on 3000
- [ ] Backend health check passes
- [ ] Frontend loads in browser
- [ ] Can navigate to http://localhost:3000/login
- [ ] Can navigate to http://localhost:3000/signup
- [ ] Login redirects to /dashboard/tasks (NOT 404)
- [ ] Signup redirects to /dashboard/tasks (NOT 404)

---

## Running the Application

### For Development

**Terminal 1 (Backend)**:
```bash
cd backend
python -m uvicorn src.app.main:app --reload --port 8000
```

**Terminal 2 (Frontend)**:
```bash
cd frontend
npm run dev -- --port 3000
```

**Open**: http://localhost:3000

### For Production Build

**Frontend**:
```bash
cd frontend
npm run build
npm start
```

**Backend**:
```bash
cd backend
python -m uvicorn src.app.main:app --port 8000 --workers 4
```

---

## Quick Reference Commands

```bash
# Check if ports are free
netstat -ano | find ":3000"
netstat -ano | find ":8000"

# Kill all Node processes
taskkill /IM node.exe /F

# Kill all Python processes
taskkill /IM python.exe /F

# Start backend
cd backend && python -m uvicorn src.app.main:app --reload --port 8000

# Start frontend
cd frontend && npm run dev -- --port 3000

# Test backend
curl http://localhost:8000/health

# Access application
# Open browser to: http://localhost:3000
```

---

## Next Steps

1. **Close all terminals**
2. **Kill all Node/Python processes** (use Task Manager or Command Prompt)
3. **Wait 5 seconds**
4. **Open fresh terminals**
5. **Start backend first** (keep it running)
6. **Start frontend second** (keep it running)
7. **Test at http://localhost:3000**

---

**Status**: Ready for clean start
**Expected**: Backend on 8000, Frontend on 3000
**Test**: http://localhost:3000 should load without 404

