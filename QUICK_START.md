# Quick Start Guide - Phase 2 Complete

**Last Updated**: December 30, 2025
**Current Status**: Code Generation Complete - Ready for Testing
**Estimated Time**: 15-20 minutes to get running

---

## In 5 Minutes: Start the Stack

### 1. Start PostgreSQL

```bash
# Using Docker (recommended)
docker run --name hackathon-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=hackathon_todo \
  -p 5432:5432 \
  -d postgres:14-alpine
```

### 2. Start Backend

```bash
cd backend

# If dependencies not installed yet:
pip install fastapi sqlmodel sqlalchemy alembic psycopg2-binary pydantic pydantic-settings python-jose passlib python-multipart python-dotenv uvicorn

# Start server
uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### 3. Start Frontend

```bash
cd frontend
npm install  # Only needed once
npm run dev
```

Expected output:
```
▲ Next.js 14.0.0
- Local: http://localhost:3000
```

### 4. Open Browser

```
Frontend:  http://localhost:3000
API Docs:  http://localhost:8000/api/docs
Health:    http://localhost:8000/health
```

---

## What's Already Done

✅ **Backend** (30+ files)
- FastAPI app with 13 API endpoints
- SQLModel ORM with 3 tables
- JWT authentication
- Password hashing
- All schemas and services
- Ready to connect to PostgreSQL

✅ **Frontend** (40+ files)
- Next.js 14 App Router
- React Context API for state
- 5 custom hooks
- 10+ React components
- Full TypeScript coverage
- Styling with Tailwind CSS

✅ **Documentation** (5 guides)
- PROJECT_STATUS_REPORT.md - Complete status overview
- DATABASE_SETUP_GUIDE.md - Database setup instructions
- IMPLEMENTATION_CHECKLIST.md - Phase 2 checklist
- BACKEND_VERIFICATION_REPORT.md - Backend verification
- This Quick Start guide

---

## Test the Stack

### Test Backend API

```bash
# 1. Sign up
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@example.com",
    "username":"testuser",
    "full_name":"Test User",
    "password":"Password123!"
  }'

# 2. Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@example.com",
    "password":"Password123!"
  }'

# 3. Copy the access_token from response and use it
TOKEN="<paste-access-token-here>"

# 4. Create a task
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"My First Task",
    "priority":"high"
  }'

# 5. List tasks
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/tasks
```

### Test Frontend UI

1. Go to http://localhost:3000
2. Click "Sign Up"
3. Fill form:
   - Email: test@example.com
   - Full Name: Test User
   - Password: Password123!
   - Confirm: Password123!
4. Click Sign Up
5. Should redirect to dashboard
6. Click "Create Task" button
7. Add task details and create
8. See task in the list

---

## Directory Structure

```
hackathon-todo/
├── backend/                    # FastAPI backend
│   ├── src/app/
│   │   ├── main.py            # Entry point
│   │   ├── config.py          # Settings
│   │   ├── database.py        # DB connection
│   │   ├── security.py        # Auth utils
│   │   ├── db/models/         # SQL models
│   │   ├── schemas/           # Request/response
│   │   ├── services/          # Business logic
│   │   └── api/v1/            # Endpoints
│   ├── pyproject.toml         # Config
│   └── setup.py
│
├── frontend/                   # Next.js frontend
│   ├── src/app/
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Home page
│   │   ├── (auth)/            # Auth pages
│   │   └── (dashboard)/       # Dashboard pages
│   ├── src/components/        # React components
│   ├── src/hooks/             # Custom hooks
│   ├── src/context/           # Context providers
│   ├── src/services/          # API calls
│   └── package.json
│
├── specs/                      # Specifications
│   └── phase2/
│       ├── specify.md         # API spec
│       ├── plan.md            # Architecture
│       └── tasks.md           # Task list
│
└── Documentation files (guides)
```

---

## API Endpoints

### Authentication (5 endpoints)
```
POST   /api/v1/auth/register    - Create new user
POST   /api/v1/auth/login       - Get tokens
POST   /api/v1/auth/refresh     - Refresh access token
POST   /api/v1/auth/logout      - Invalidate token
GET    /api/v1/auth/me          - Current user info
```

### Tasks (5 endpoints)
```
GET    /api/v1/tasks            - List user's tasks
POST   /api/v1/tasks            - Create task
GET    /api/v1/tasks/{id}       - Get task details
PATCH  /api/v1/tasks/{id}       - Update task
DELETE /api/v1/tasks/{id}       - Delete task
```

### Users (2 endpoints)
```
GET    /api/v1/users/profile    - Get user profile
PATCH  /api/v1/users/profile    - Update profile
```

### Health (1 endpoint)
```
GET    /health                  - Health check
```

---

## Common Commands

### Database
```bash
# Check PostgreSQL running
docker ps

# Stop database
docker stop hackathon-postgres

# Remove database container (careful!)
docker rm hackathon-postgres

# View database
psql -h localhost -U postgres -d hackathon_todo
```

### Backend
```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Start server
uvicorn src.app.main:app --reload

# Stop server (Ctrl+C)
# Restart with source code changes (auto-reload enabled)

# Test imports
python -c "from src.app.main import app; print('OK')"
```

### Frontend
```bash
# Install dependencies
cd frontend
npm install

# Start dev server
npm run dev

# Stop dev server (Ctrl+C)

# Build for production
npm run build

# Run production build locally
npm run preview

# Type check
npm run type-check
```

---

## Environment Files

### Backend (.env or .env.development)
```
DATABASE_URL=postgresql://postgres:postgres@localhost/hackathon_todo
JWT_SECRET_KEY=dev-secret-key-for-testing-only-minimum-32-chars-long
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
DEBUG=False
ENVIRONMENT=development
```

Default values are built in - `.env` is optional for development.

### Frontend
No `.env` needed for development. Uses localhost:8000 API by default.

---

## Verify Everything Works

Run this checklist:

```bash
# 1. Check database
docker ps | grep postgres  # Should show running container

# 2. Check backend
curl http://localhost:8000/health  # Should return {"status":"ok"}

# 3. Check API docs
# Visit http://localhost:8000/api/docs in browser
# Should see Swagger UI with all endpoints

# 4. Check frontend
# Visit http://localhost:3000 in browser
# Should see landing page
```

---

## Troubleshooting Quick Answers

| Problem | Solution |
|---------|----------|
| "Could not connect to database" | Start PostgreSQL: `docker run ...` (see above) |
| "Port 5432 already in use" | Stop other PostgreSQL: `docker stop hackathon-postgres` |
| "Port 8000 already in use" | Change port: `uvicorn ... --port 8001` |
| "Port 3000 already in use" | Next.js will ask to use 3001 instead, or `npm run dev -- -p 3001` |
| "No module named 'fastapi'" | Install dependencies: `pip install fastapi ...` |
| "Module not found errors" | Run `npm install` in frontend directory |
| "CORS error in browser" | Ensure backend is running on port 8000 |
| "JWT_SECRET_KEY must be at least 32 characters" | Update .env with longer key |
| "DATABASE_URL must be a valid PostgreSQL connection string" | Check DATABASE_URL format in .env |

---

## What to Do Next

### Option A: Test Everything (Recommended)
1. Follow "Test the Stack" section above
2. Complete manual signup/login/task workflow
3. Check IMPLEMENTATION_CHECKLIST.md for detailed tests

### Option B: Skip to Specific Task
- **Database Issues**: See DATABASE_SETUP_GUIDE.md
- **Backend Problems**: See backend/CLAUDE.md
- **Frontend Problems**: See frontend/CLAUDE.md
- **Need Full Overview**: See PROJECT_STATUS_REPORT.md

### Option C: Jump to Phase 3
Once Phase 2 is fully tested, move to advanced features:
- Categories and projects
- Task sharing
- Comments
- Advanced search
- Notifications

---

## Key Decisions Already Made

✅ **FastAPI** for backend (chosen for simplicity and performance)
✅ **SQLModel** for ORM (combines SQLAlchemy + Pydantic)
✅ **Next.js 14 App Router** for frontend (modern React)
✅ **PostgreSQL** for database (reliable, open-source)
✅ **JWT** for authentication (stateless, scalable)
✅ **React Context API** for state (no Redux overhead)
✅ **Tailwind CSS** for styling (utility-first)

All decisions follow specifications in `specs/phase2/specify.md`

---

## File Counts

| Component | Files | Status |
|-----------|-------|--------|
| Backend | 30+ | ✅ Complete |
| Frontend | 40+ | ✅ Complete |
| Documentation | 5+ | ✅ Complete |
| Specifications | 3 | ✅ Complete |
| **Total** | **80+** | **✅ Complete** |

---

## Help & Resources

### Quick Links
- API Docs: http://localhost:8000/api/docs (when backend running)
- Frontend: http://localhost:3000 (when frontend running)
- Project Status: PROJECT_STATUS_REPORT.md
- Database Help: DATABASE_SETUP_GUIDE.md
- Implementation Tasks: IMPLEMENTATION_CHECKLIST.md
- Backend Guide: backend/CLAUDE.md
- Frontend Guide: frontend/CLAUDE.md
- API Specs: specs/phase2/specify.md

### Support
If something doesn't work:
1. Check the relevant guide above
2. Review troubleshooting section
3. Check console/terminal for error messages
4. Verify all services running: `docker ps`, backend logs, browser console

---

## Next Checkpoint

**Goal**: Have all three running and connected (database → backend → frontend)

**Success Criteria**:
- ✅ PostgreSQL running (docker ps shows container)
- ✅ Backend running (can access http://localhost:8000/health)
- ✅ Frontend running (can access http://localhost:3000)
- ✅ Can signup through frontend
- ✅ Can create task through frontend
- ✅ Task appears in database

**Estimated Time**: 20 minutes

---

## One-Line Commands Reference

```bash
# Start everything
docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:14-alpine && \
cd backend && uvicorn src.app.main:app --reload &
cd frontend && npm run dev

# Stop everything
docker stop hackathon-postgres
pkill -f uvicorn
pkill -f "next dev"

# Test API
curl -X POST http://localhost:8000/api/v1/auth/register -H "Content-Type: application/json" -d '{"email":"test@example.com","username":"testuser","full_name":"Test User","password":"Password123!"}'

# View database
psql -h localhost -U postgres -d hackathon_todo -c "SELECT COUNT(*) as users FROM users; SELECT COUNT(*) as tasks FROM tasks;"
```

---

## Important Notes

⚠️ **First Time Setup**: Expect 5-10 minutes for dependencies to install
⚠️ **Database Required**: PostgreSQL must be running before backend starts
⚠️ **Ports**: Uses 5432 (DB), 8000 (Backend), 3000 (Frontend)
⚠️ **Defaults**: Development environment variables are built-in, no `.env` needed
⚠️ **Password Format**: Must be at least 8 characters, alphanumeric (tested on signup)

---

**Generated**: December 30, 2025
**Phase**: 2 - Core API Implementation
**Status**: 🟢 Ready for Testing

---

## Copy-Paste Start

```bash
# Terminal 1: Database
docker run --name hackathon-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=hackathon_todo -p 5432:5432 -d postgres:14-alpine

# Terminal 2: Backend
cd backend
pip install fastapi sqlmodel sqlalchemy alembic psycopg2-binary pydantic pydantic-settings python-jose passlib python-multipart python-dotenv uvicorn
uvicorn src.app.main:app --reload

# Terminal 3: Frontend
cd frontend
npm install
npm run dev

# Browser
# http://localhost:3000  (frontend)
# http://localhost:8000/api/docs (API docs)
```

Done! You're running the full stack. 🎉

