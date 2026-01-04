# Quick Start - Phase II Todo App

## 🚀 Start in 5 Minutes

### Option 1: Docker Compose (Easiest)

```bash
cd F:\GIAIC\ HACKATHONS\FULL\ STACK\ WEB\ APP\hackathon-todo
docker-compose up
```

Then open:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

### Option 2: Local Development

**Terminal 1 - Backend:**
```bash
cd F:\GIAIC\ HACKATHONS\FULL\ STACK\ WEB\ APP\hackathon-todo\backend
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env.development
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd F:\GIAIC\ HACKATHONS\FULL\ STACK\ WEB\ APP\hackathon-todo\frontend
npm install
cp .env.local.example .env.local
npm run dev
```

---

## 📝 Test the App

### Create Account
1. Go to http://localhost:3000
2. Click "Sign Up"
3. Enter email, name, password
4. Click "Sign Up"

### Create a Task
1. Click "+ New Task" on dashboard
2. Enter title, description, priority, due date
3. Click "Create Task"

### View API Documentation
1. Go to http://localhost:8000/api/docs
2. Try out endpoints with Swagger UI

---

## 🛠️ Key Files

| File | Purpose |
|------|---------|
| `backend/src/app/main.py` | FastAPI app |
| `backend/src/app/api/v1/` | All endpoints |
| `frontend/src/app/` | All pages |
| `frontend/src/components/` | React components |
| `docker-compose.yml` | Full stack |

---

## 🔌 API Examples

### Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "Password123!",
    "full_name": "John Doe"
  }'
```

### Create Task
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": "high",
    "due_date": "2025-12-31"
  }'
```

---

## 📚 More Info

- **Full Documentation**: See `PHASE2_READY_TO_RUN.md`
- **Architecture**: See `specs/phase2/plan.md`
- **API Reference**: http://localhost:8000/api/docs (when running)
- **Specifications**: See `specs/phase2/specify.md`

---

## ✅ That's It!

Your full-stack multi-user todo app is ready to use! 🎉

**Backend**: http://localhost:8000
**Frontend**: http://localhost:3000
