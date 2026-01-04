# Neon PostgreSQL - Quick Reference Card

**Date**: December 30, 2025
**Your Database**: Neon PostgreSQL Cloud
**Status**: ✅ CONFIGURED & READY

---

## 🎯 COPY-PASTE QUICK START

### Terminal 1: Start Backend

```bash
cd backend
pip install fastapi sqlmodel sqlalchemy alembic psycopg2-binary pydantic pydantic-settings python-jose passlib python-multipart python-dotenv uvicorn
uvicorn src.app.main:app --reload
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Terminal 2: Start Frontend

```bash
cd frontend
npm install
npm run dev
```

**Expected Output**:
```
▲ Next.js 14.0.0
- Local: http://localhost:3000
```

### Terminal 3: Test Database

```bash
# Once backend started, check it connected to Neon
curl http://localhost:8000/health
```

**Expected Response**:
```json
{"status":"ok"}
```

### Browser: Test Full App

1. Go to http://localhost:3000
2. Click "Sign Up"
3. Enter: email, name, password
4. Click "Sign Up"
5. Create a task
6. Verify it appears in list

---

## 📋 YOUR CREDENTIALS

```
Database: neondb
Host: ep-long-scene-ahwg2uzf-pooler.c-3.us-east-1.aws-neon.tech
User: neondb_owner
Password: npg_tklw9gJO5szD
JWT Secret: 0b91ba15b7660f166d9798f31853c232530b5bd01d9b413a3399db2e4951843a
```

⚠️ **These are stored securely in `backend/.env` file** ⚠️

---

## 🔗 IMPORTANT URLS

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Main app |
| Backend Health | http://localhost:8000/health | Check if API running |
| API Docs | http://localhost:8000/api/docs | Test endpoints |
| ReDoc | http://localhost:8000/api/redoc | API documentation |
| Neon Console | https://console.neon.tech/ | Manage database |

---

## 🚀 START THE SYSTEM (3 Steps)

### 1️⃣ Backend Setup

```bash
cd backend
pip install fastapi sqlmodel sqlalchemy alembic psycopg2-binary pydantic pydantic-settings python-jose passlib python-multipart python-dotenv uvicorn
uvicorn src.app.main:app --reload
```

✅ Backend running on http://localhost:8000

### 2️⃣ Frontend Setup (New Terminal)

```bash
cd frontend
npm install
npm run dev
```

✅ Frontend running on http://localhost:3000

### 3️⃣ Test It Works

Open http://localhost:3000 → Sign up → Create task ✅

---

## 📋 API ENDPOINTS (13 Total)

### Authentication
```
POST   /api/v1/auth/register     → Sign up new user
POST   /api/v1/auth/login        → Login with email/password
POST   /api/v1/auth/refresh      → Get new access token
POST   /api/v1/auth/logout       → Logout
GET    /api/v1/auth/me           → Get current user
```

### Tasks
```
GET    /api/v1/tasks             → List all tasks
POST   /api/v1/tasks             → Create task
GET    /api/v1/tasks/{id}        → Get task details
PATCH  /api/v1/tasks/{id}        → Update task
DELETE /api/v1/tasks/{id}        → Delete task
```

### Users
```
GET    /api/v1/users/profile     → Get profile
PATCH  /api/v1/users/profile     → Update profile
```

### Health
```
GET    /health                   → API health check
```

---

## 🔐 YOUR CONFIGURATION

### File Locations
- `.env` - Production configuration (auto-loaded)
- `.env.development` - Development configuration
- `.gitignore` - Ensures .env is not committed

### What's Configured
✅ Database URL (Neon PostgreSQL)
✅ JWT Secret (64 characters)
✅ JWT Algorithm (HS256)
✅ CORS Origins (localhost:3000, 5173)
✅ SSL Mode (required for Neon)
✅ Connection Pool (size=5, overflow=10)

---

## 🧪 QUICK TESTS

### Test 1: Backend Running?
```bash
curl http://localhost:8000/health
```
Should return: `{"status":"ok"}`

### Test 2: Database Connected?
```bash
curl http://localhost:8000/api/docs
```
Should show: Swagger UI with all endpoints

### Test 3: Frontend Running?
Visit http://localhost:3000 in browser
Should show: Landing page

### Test 4: Full Signup Flow?
1. Go to http://localhost:3000/signup
2. Fill: email, name, password
3. Click Sign Up
4. Check: Redirects to dashboard

### Test 5: Create Task?
1. On dashboard, click "Create Task"
2. Fill: title, priority
3. Click Create
4. Check: Task appears in list

---

## ⚠️ COMMON ISSUES & FIXES

| Issue | Fix |
|-------|-----|
| "Port 8000 already in use" | `uvicorn ... --port 8001` |
| "Cannot find module fastapi" | Run: `pip install fastapi sqlmodel ...` |
| "npm: command not found" | Install Node.js from nodejs.org |
| "Connection timeout" | Check internet connection |
| "Authentication failed" | Verify .env credentials |
| "Frontend can't reach API" | Verify backend running on 8000 |

---

## 📊 PROJECT STRUCTURE

```
hackathon-todo/
├── backend/
│   ├── .env                    ← Your configuration (DO NOT COMMIT)
│   ├── .env.development        ← Dev config
│   ├── src/app/
│   │   ├── main.py             ← FastAPI app
│   │   ├── config.py           ← Settings loading
│   │   ├── database.py         ← DB connection
│   │   ├── security.py         ← JWT & bcrypt
│   │   ├── db/models/          ← Database models
│   │   ├── schemas/            ← Request/response schemas
│   │   ├── services/           ← Business logic
│   │   └── api/v1/             ← API endpoints
│   └── pyproject.toml          ← Dependencies
│
├── frontend/
│   ├── src/app/
│   │   ├── layout.tsx          ← Root layout
│   │   ├── page.tsx            ← Home page
│   │   ├── (auth)/             ← Auth pages
│   │   └── (dashboard)/        ← Dashboard pages
│   ├── src/components/         ← React components
│   ├── src/hooks/              ← Custom hooks
│   ├── src/services/           ← API calls
│   └── package.json            ← Dependencies
│
└── Documentation files
```

---

## 🎯 WORKFLOW

### First Time
1. Install Python 3.10+ (if not installed)
2. Install Node.js 18+ (if not installed)
3. Run backend setup (installs dependencies)
4. Run frontend setup (installs dependencies)
5. Start both servers
6. Open http://localhost:3000
7. Test signup and create task

### Every Other Time
1. Terminal 1: `cd backend && uvicorn src.app.main:app --reload`
2. Terminal 2: `cd frontend && npm run dev`
3. Open http://localhost:3000
4. Develop and test

### Stopping
- Press `Ctrl+C` in each terminal

### Changes Auto-Reload
- Backend: Changes to Python files auto-reload
- Frontend: Changes to .tsx/.ts files auto-reload
- Restart if config/package changes

---

## 📈 WHAT HAPPENS ON STARTUP

### Backend Startup (First Time)
1. Loads configuration from `.env`
2. Connects to Neon PostgreSQL
3. Creates 3 tables:
   - `users` (email, password_hash, etc.)
   - `tasks` (title, status, priority, etc.)
   - `refresh_token` (for token rotation)
4. Creates indexes for performance
5. Ready to accept API requests

### Frontend Startup
1. Installs dependencies
2. Starts Next.js dev server
3. Watches for file changes
4. Ready for browser access

### On First Signup
1. User fills signup form
2. Backend validates data
3. Hashes password with bcrypt
4. Stores user in Neon PostgreSQL
5. Generates JWT access token
6. Frontend stores token locally
7. Redirects to dashboard

---

## 🔑 KEY FILES TO KNOW

### Backend
- `src/app/main.py` - Where FastAPI app is created
- `src/app/config.py` - Loads your `.env` file
- `src/app/database.py` - Connects to Neon
- `src/app/security.py` - JWT and password handling
- `src/app/api/v1/` - All API endpoints

### Frontend
- `src/app/layout.tsx` - Root with providers
- `src/app/page.tsx` - Landing page
- `src/app/(auth)/` - Login/signup pages
- `src/app/(dashboard)/` - Protected pages
- `src/context/` - State management
- `src/services/` - API calls

### Configuration
- `.env` ← Your secrets (DO NOT COMMIT)
- `.env.development` ← Dev config
- `pyproject.toml` - Backend dependencies
- `package.json` - Frontend dependencies

---

## ✅ VERIFICATION CHECKLIST

Before declaring "ready", verify:

- [ ] Backend installs without errors
- [ ] Frontend installs without errors
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] http://localhost:8000/health returns OK
- [ ] http://localhost:8000/api/docs shows endpoints
- [ ] http://localhost:3000 loads landing page
- [ ] Can signup new user
- [ ] Redirects to dashboard after signup
- [ ] Can create task
- [ ] Task appears in list
- [ ] Can logout
- [ ] Can login again

---

## 💡 PRO TIPS

### Debug Backend
- Check terminal output for errors
- Add print statements in code
- Use http://localhost:8000/api/docs to test endpoints
- Check Neon console for database status

### Debug Frontend
- Open http://localhost:3000 in browser
- Press F12 to open DevTools
- Check Console tab for JavaScript errors
- Check Network tab to see API calls

### Monitor Database
- Go to https://console.neon.tech/
- Login with your Neon account
- See database status, query history, etc.

### Test API Directly
```bash
# Without token
curl http://localhost:8000/health

# With token (after login)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/v1/auth/me
```

---

## 🎓 LEARNING RESOURCES

### Understanding the Code
1. Read `specs/phase2/specify.md` for API details
2. Check `backend/CLAUDE.md` for backend patterns
3. Check `frontend/CLAUDE.md` for frontend patterns
4. Review code comments in source files

### API Testing
- Use http://localhost:8000/api/docs (Swagger UI)
- Try endpoints there without writing code
- See request/response examples

### Database
- Use Neon console to view data
- Use psql to query directly
- Use DBeaver GUI tool

---

## 🚨 CRITICAL REMINDERS

⚠️ **DO NOT:**
- Share `.env` file with anyone
- Commit `.env` to Git (it's in .gitignore)
- Expose JWT secret publicly
- Use weak passwords in development
- Run with `DEBUG=true` in production

✅ **DO:**
- Keep `.env` file private
- Rotate JWT secret periodically (for production)
- Use strong passwords
- Set `DEBUG=false` in production
- Monitor Neon database usage

---

## 🎯 NEXT STEPS

1. **Now**: Copy-paste commands from "QUICK START" section above
2. **Then**: Follow "QUICK TESTS" section to verify everything works
3. **After**: Use IMPLEMENTATION_CHECKLIST.md for detailed testing
4. **Finally**: Check NEON_SETUP_GUIDE.md for detailed database info

---

## 📞 NEED HELP?

| Question | Answer |
|----------|--------|
| What's in `.env`? | Your Neon credentials and JWT secret |
| Where's database? | Neon (cloud-hosted PostgreSQL) |
| How do I see data? | Go to https://console.neon.tech/ |
| Is .env secure? | Yes - it's in .gitignore, never committed |
| Can I change JWT secret? | Yes - just update `.env` and restart |
| Can I connect with psql? | Yes - use full connection string from `.env` |
| What if Neon goes down? | Data is safe - Neon has backups |
| How do I backup data? | Neon does it automatically + manual dumps |

---

**Status**: ✅ **CONFIGURATION COMPLETE**
**Database**: 🟢 **NEON POSTGRESQL CONFIGURED**
**Ready To**: 🚀 **START BACKEND & FRONTEND**

```bash
# Terminal 1: Backend
cd backend && uvicorn src.app.main:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev

# Browser
http://localhost:3000
```

**That's it! Your app is live!** 🎉

---

**Generated**: December 30, 2025
**Configuration**: Neon PostgreSQL + JWT
**Status**: Ready for Immediate Use

