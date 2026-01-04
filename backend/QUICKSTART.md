# Quick Start Guide - Hackathon Todo Backend

Get the backend API running in 5 minutes.

## Option 1: Using Docker Compose (Recommended)

### Prerequisites
- Docker and Docker Compose installed

### Steps

```bash
# 1. Navigate to project root
cd hackathon-todo

# 2. Start all services
docker-compose up -d

# 3. Check services are running
docker-compose ps

# 4. View logs
docker-compose logs -f backend

# 5. Test the API
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

### API is available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- Database: localhost:5432

### Stop services
```bash
docker-compose down
```

---

## Option 2: Local Development Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 12+ (running locally)
- pip or poetry

### Steps

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -e ".[dev]"

# 5. Setup environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# 6. Run the application
uvicorn app.main:app --reload
```

### API is available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

---

## First API Call

### 1. Register a user

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123",
    "full_name": "John Doe"
  }'
```

Response includes:
- `access_token`: Use this for authenticated requests
- `refresh_token`: Use to get new access token
- `user`: User information

### 2. Save the access token
```bash
export TOKEN="<access_token_from_response>"
```

### 3. Create a task

```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project",
    "description": "Finish the backend API",
    "priority": "high",
    "due_date": "2025-12-31T23:59:59"
  }'
```

### 4. List your tasks

```bash
curl -X GET "http://localhost:8000/api/v1/tasks?skip=0&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

### 5. Get your profile

```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

---

## Using Swagger UI

Instead of curl, you can use the interactive Swagger UI:

1. Open http://localhost:8000/api/docs
2. Click "Authorize" button
3. Enter: `Bearer <your_access_token>`
4. Try any endpoint

---

## Common Issues & Solutions

### Issue: Port 8000 already in use

**Solution**: Change port in .env or use:
```bash
uvicorn app.main:app --port 8001
```

### Issue: PostgreSQL connection refused

**Check**:
1. PostgreSQL is running
2. Connection string in .env is correct
3. Database exists or will be auto-created

**With Docker Compose**:
```bash
docker-compose logs postgres
```

### Issue: Module not found error

**Solution**: Make sure you're in the right directory and virtual environment is activated

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### Issue: Database tables don't exist

**Solution**: Tables are auto-created on startup. If not:

```bash
python -c "from app.database import create_db_and_tables; create_db_and_tables()"
```

---

## Next Steps

1. **Read the full README**: `backend/README.md`
2. **View implementation details**: `backend/IMPLEMENTATION_SUMMARY.md`
3. **Start the frontend**: See frontend setup guide
4. **Run tests**: `pytest`
5. **Deploy**: Follow deployment section in README

---

## Development Commands

### Run with auto-reload
```bash
uvicorn app.main:app --reload
```

### Format code
```bash
black .
isort .
```

### Run linting
```bash
flake8 src/
mypy src/
```

### Run tests
```bash
pytest
pytest -v  # Verbose
pytest --cov  # With coverage
```

### View API schema
```
GET http://localhost:8000/api/openapi.json
```

---

## Quick Reference

### Auth Endpoints
- `POST /api/v1/auth/register` - Create account
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Get new access token
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/logout` - Logout

### User Endpoints
- `GET /api/v1/users/profile` - Get profile
- `PATCH /api/v1/users/profile` - Update profile
- `PUT /api/v1/users/password` - Change password

### Task Endpoints
- `GET /api/v1/tasks` - List tasks
- `POST /api/v1/tasks` - Create task
- `GET /api/v1/tasks/{id}` - Get task
- `PATCH /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task

### Health
- `GET /health` - Health check
- `GET /api/docs` - Swagger UI
- `GET /api/redoc` - ReDoc documentation

---

## Key Features

- ✅ User authentication with JWT
- ✅ Task management with CRUD operations
- ✅ Pagination and filtering
- ✅ Type-safe database models
- ✅ Comprehensive error handling
- ✅ CORS support
- ✅ Docker ready
- ✅ Production configuration

---

## Need Help?

1. Check README.md for detailed documentation
2. View IMPLEMENTATION_SUMMARY.md for architecture
3. Check Swagger UI at /api/docs for endpoint details
4. Look at example requests in README.md

Happy coding!
