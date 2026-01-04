# Hackathon Todo API - Backend

Multi-user todo application backend API built with FastAPI, SQLModel, and PostgreSQL.

## Features

- User authentication with JWT tokens
- Refresh token mechanism for long-lived sessions
- User profile management
- Todo CRUD operations with filtering and pagination
- Type-safe database models with SQLModel
- Comprehensive error handling
- CORS support for frontend integration
- PostgreSQL database with proper schema
- Docker support for containerized deployment

## Tech Stack

- **Framework**: FastAPI 0.109.0
- **ORM**: SQLModel 0.0.14 (SQLAlchemy 2.0)
- **Database**: PostgreSQL 16
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt via passlib
- **Configuration**: pydantic-settings
- **Database Migrations**: Alembic

## Project Structure

```
backend/
├── src/app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py         # Authentication endpoints
│   │       ├── users.py        # User management endpoints
│   │       ├── tasks.py        # Task CRUD endpoints
│   │       ├── health.py       # Health check endpoint
│   │       └── __init__.py     # Router configuration
│   ├── db/
│   │   └── models/
│   │       ├── base.py         # Base model with common fields
│   │       ├── user.py         # User database model
│   │       ├── task.py         # Task database model
│   │       ├── refresh_token.py # Refresh token model
│   │       └── __init__.py
│   ├── services/
│   │   ├── auth.py            # Authentication business logic
│   │   ├── user.py            # User service methods
│   │   ├── task.py            # Task service methods
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── auth.py            # Auth request/response schemas
│   │   ├── user.py            # User schemas
│   │   ├── task.py            # Task schemas
│   │   └── __init__.py
│   ├── config.py              # Configuration management
│   ├── database.py            # Database setup and session
│   ├── dependencies.py        # FastAPI dependencies
│   ├── security.py            # Password hashing and JWT
│   ├── main.py                # FastAPI application
│   └── __init__.py
├── pyproject.toml             # Project dependencies
├── Dockerfile                 # Docker image definition
├── alembic.ini               # Database migration config
├── .env.example              # Example environment variables
└── README.md
```

## Setup

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- pip or poetry

### Installation

1. **Clone and navigate to backend:**

```bash
cd backend
```

2. **Create virtual environment:**

```bash
python -m venv venv

# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -e ".[dev]"
```

4. **Configure environment:**

```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

Example .env:
```
DATABASE_URL=postgresql://user:password@localhost:5432/hackathon_todo
JWT_SECRET_KEY=your-secret-key-min-32-chars
JWT_ALGORITHM=HS256
CORS_ORIGINS=http://localhost:3000
DEBUG=true
```

5. **Run application:**

```bash
uvicorn app.main:app --reload
```

API will be available at `http://localhost:8000`

## Docker Setup

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

Services:
- Backend API: http://localhost:8000
- PostgreSQL: localhost:5432
- API Docs: http://localhost:8000/api/docs

### Manual Docker Build

```bash
# Build image
docker build -t hackathon-todo-api .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:password@localhost:5432/db \
  hackathon-todo-api
```

## API Endpoints

### Health Check

```http
GET /health
```

Response: `{"status": "healthy"}`

### Authentication

#### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure-password",
  "full_name": "John Doe"
}
```

Response (201):
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "avatar_url": null,
    "is_active": true,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure-password"
}
```

Response (200): Same as register

#### Refresh Token
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Get Current User
```http
GET /api/v1/auth/me
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### Logout
```http
POST /api/v1/auth/logout
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### User Management

#### Get Profile
```http
GET /api/v1/users/profile
Authorization: Bearer <access_token>
```

#### Update Profile
```http
PATCH /api/v1/users/profile
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "full_name": "Jane Doe",
  "avatar_url": "https://example.com/avatar.jpg"
}
```

#### Change Password
```http
PUT /api/v1/users/password
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "old_password": "current-password",
  "new_password": "new-password"
}
```

### Tasks

#### List Tasks (with pagination and filtering)
```http
GET /api/v1/tasks?skip=0&limit=10&status=pending&priority=high
Authorization: Bearer <access_token>
```

Query Parameters:
- `skip`: Number of items to skip (default: 0)
- `limit`: Items per page (default: 10, max: 100)
- `status`: Filter by status (pending, completed)
- `priority`: Filter by priority (low, medium, high)

Response:
```json
{
  "items": [...],
  "total": 5,
  "skip": 0,
  "limit": 10
}
```

#### Create Task
```http
POST /api/v1/tasks
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Complete project",
  "description": "Finish the backend API",
  "priority": "high",
  "due_date": "2024-12-31T23:59:59"
}
```

Response (201):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "550e8400-e29b-41d4-a716-446655440001",
  "title": "Complete project",
  "description": "Finish the backend API",
  "status": "pending",
  "priority": "high",
  "due_date": "2024-12-31T23:59:59",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "completed_at": null
}
```

#### Get Task
```http
GET /api/v1/tasks/{task_id}
Authorization: Bearer <access_token>
```

#### Update Task
```http
PATCH /api/v1/tasks/{task_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Updated title",
  "status": "completed",
  "priority": "medium"
}
```

#### Delete Task
```http
DELETE /api/v1/tasks/{task_id}
Authorization: Bearer <access_token>
```

Response (204): No content

## Authentication

All authenticated endpoints require the `Authorization` header:

```
Authorization: Bearer <access_token>
```

Access tokens are valid for 24 hours. Use refresh token to get a new access token when it expires.

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
isort .
```

### Linting

```bash
flake8 src/
mypy src/
```

### Database Migrations

Using Alembic:

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Production Deployment

1. Set environment variables for production
2. Build Docker image
3. Deploy using docker-compose or orchestration platform
4. Configure PostgreSQL for production
5. Set up backup strategy
6. Enable HTTPS/SSL
7. Configure firewall and security groups

Example production .env:
```
DATABASE_URL=postgresql://user:strong-password@db.example.com/prod_db
JWT_SECRET_KEY=production-secret-key-32-chars-minimum!
DEBUG=false
ENVIRONMENT=production
CORS_ORIGINS=https://example.com,https://www.example.com
```

## Error Handling

All errors return proper HTTP status codes with error details:

```json
{
  "detail": "Error message"
}
```

Common status codes:
- 200: Success
- 201: Created
- 204: No content (successful delete)
- 400: Bad request (validation error)
- 401: Unauthorized (missing/invalid token)
- 403: Forbidden (user inactive)
- 404: Not found
- 500: Internal server error

## Security

- Passwords are hashed with bcrypt (10 rounds)
- JWT tokens signed with HS256
- CORS properly configured
- SQL injection prevented by using SQLModel ORM
- Input validation on all endpoints
- Users can only access their own data

## Database

### Schema

**users table:**
- id (UUID, PK)
- email (VARCHAR, unique)
- username (VARCHAR, unique)
- password_hash (VARCHAR)
- full_name (VARCHAR)
- avatar_url (VARCHAR, nullable)
- is_active (BOOLEAN)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

**tasks table:**
- id (UUID, PK)
- user_id (UUID, FK)
- title (VARCHAR)
- description (TEXT, nullable)
- status (ENUM: pending, completed)
- priority (ENUM: low, medium, high)
- due_date (TIMESTAMP, nullable)
- completed_at (TIMESTAMP, nullable)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

**refresh_tokens table:**
- id (UUID, PK)
- user_id (UUID, FK)
- token (VARCHAR, unique)
- expires_at (TIMESTAMP)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

## License

MIT
