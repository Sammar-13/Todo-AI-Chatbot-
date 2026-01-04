# Database Setup & Configuration Guide

**Purpose**: Complete guide to setting up PostgreSQL database for the Hackathon Todo Application
**Last Updated**: December 30, 2025
**Status**: Ready for Implementation

---

## Quick Start (5 minutes)

### Option 1: Docker (Recommended - Fastest)

```bash
# Create and start PostgreSQL container
docker run --name hackathon-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=hackathon_todo \
  -p 5432:5432 \
  -d postgres:14-alpine

# Verify connection
psql -h localhost -U postgres -d hackathon_todo -c "SELECT 1;"

# Expected output: SUCCESS
```

### Option 2: Docker Compose (Best for Full Stack)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14-alpine
    container_name: hackathon-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: hackathon_todo
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: hackathon-backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/hackathon_todo
      JWT_SECRET_KEY: dev-secret-key-for-testing-only-minimum-32-chars-long
    depends_on:
      postgres:
        condition: service_healthy
    command: uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: hackathon-frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000/api
    depends_on:
      - backend

volumes:
  postgres_data:
```

Then run:
```bash
docker-compose up
```

### Option 3: Local PostgreSQL Installation

**Windows**:
1. Download from https://www.postgresql.org/download/windows/
2. Run installer with default settings
3. Remember the PostgreSQL password
4. Create database:
   ```bash
   psql -U postgres
   CREATE DATABASE hackathon_todo;
   \q
   ```

**macOS**:
```bash
# Using Homebrew
brew install postgresql@14
brew services start postgresql@14

# Create database
createdb hackathon_todo
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb hackathon_todo
```

---

## Detailed Setup Guide

### 1. PostgreSQL Installation

#### What You Need
- PostgreSQL 14 or higher
- Database client (psql or DBeaver)
- Network access to port 5432

#### Database Configuration

The backend expects this PostgreSQL setup:

```
Host: localhost
Port: 5432
User: postgres
Password: postgres
Database: hackathon_todo
```

If you use different credentials, update `.env`:
```bash
DATABASE_URL=postgresql://username:password@host:port/database_name
```

### 2. Database Schema Creation

The backend uses **SQLModel** which automatically creates tables on first startup. When the backend starts, it will:

1. Connect to PostgreSQL
2. Create all tables (users, tasks, refresh_tokens)
3. Create indexes
4. Initialize the schema

#### Manual Table Creation (Optional)

If you prefer to create tables manually:

```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  username VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(255) NOT NULL,
  avatar_url VARCHAR(255),
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  INDEX idx_users_email (email),
  INDEX idx_users_username (username)
);

-- Tasks table
CREATE TABLE tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(50) DEFAULT 'pending',
  priority VARCHAR(50) DEFAULT 'medium',
  due_date VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP,

  INDEX idx_tasks_user_id (user_id),
  INDEX idx_tasks_status (status),
  INDEX idx_tasks_due_date (due_date)
);

-- Refresh tokens table
CREATE TABLE refresh_token (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token VARCHAR(512) UNIQUE NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  INDEX idx_refresh_token_token (token)
);
```

### 3. Connection Verification

#### Using psql
```bash
# Connect to database
psql -h localhost -U postgres -d hackathon_todo

# List tables
\dt

# Exit
\q
```

#### Using Python
```bash
cd backend

# Test database connection
python -c "
from src.app.database import engine
from src.app.config import settings

print(f'Connecting to: {settings.DATABASE_URL}')
with engine.connect() as connection:
    result = connection.execute('SELECT 1')
    print(f'Connection successful: {result.fetchone()}')
"
```

#### Using Backend Startup
```bash
cd backend
uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000

# Expected output:
# INFO:     Started server process
# INFO:     Application startup complete
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Database Management

### Backup

#### Using Docker
```bash
# Backup database from running container
docker exec hackathon-postgres pg_dump -U postgres hackathon_todo > backup.sql

# Restore from backup
docker exec -i hackathon-postgres psql -U postgres hackathon_todo < backup.sql
```

#### Using Local PostgreSQL
```bash
# Backup
pg_dump -h localhost -U postgres hackathon_todo > backup.sql

# Restore
psql -h localhost -U postgres hackathon_todo < backup.sql
```

### Reset Database

```bash
# WARNING: This will DELETE all data

# Option 1: Drop and recreate
psql -h localhost -U postgres -c "DROP DATABASE hackathon_todo;"
psql -h localhost -U postgres -c "CREATE DATABASE hackathon_todo;"

# Option 2: Truncate tables
psql -h localhost -U postgres -d hackathon_todo -c "
  TRUNCATE refresh_token CASCADE;
  TRUNCATE tasks CASCADE;
  TRUNCATE users CASCADE;
"
```

### Monitor Database

```bash
# Connect to PostgreSQL
psql -h localhost -U postgres -d hackathon_todo

# View tables
SELECT * FROM information_schema.tables WHERE table_schema = 'public';

# Count records
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM tasks;

# View indexes
SELECT * FROM pg_indexes WHERE tablename IN ('users', 'tasks', 'refresh_token');

# Check database size
SELECT pg_size_pretty(pg_database_size('hackathon_todo'));
```

---

## Environment Configuration

### Backend (.env or environment variables)

For local development, the backend uses defaults:

```bash
# Default values (no .env file needed):
DATABASE_URL=postgresql://postgres:postgres@localhost/hackathon_todo
JWT_SECRET_KEY=dev-secret-key-for-testing-only-minimum-32-chars-long
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Using Custom .env File

Create `backend/.env`:

```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost/hackathon_todo

# JWT
JWT_SECRET_KEY=your-secret-key-minimum-32-characters-long
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24
REFRESH_TOKEN_EXPIRE_DAYS=7

# Security
BCRYPT_ROUNDS=10

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000

# Application
DEBUG=False
ENVIRONMENT=development
LOG_LEVEL=INFO
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

### Environment Variables Explained

| Variable | Purpose | Example | Notes |
|----------|---------|---------|-------|
| DATABASE_URL | PostgreSQL connection string | postgresql://user:pass@host:5432/db | Format: postgresql://username:password@host:port/database |
| JWT_SECRET_KEY | Secret for signing JWT tokens | min-32-character-secret | MUST be at least 32 characters |
| JWT_ALGORITHM | JWT signing algorithm | HS256 | Only HS256 supported currently |
| ACCESS_TOKEN_EXPIRE_HOURS | Access token expiration | 24 | Hours until access token expires |
| REFRESH_TOKEN_EXPIRE_DAYS | Refresh token expiration | 7 | Days until refresh token expires |
| BCRYPT_ROUNDS | Password hashing complexity | 10 | Higher = more secure but slower |
| CORS_ORIGINS | Allowed frontend origins | http://localhost:3000 | Comma-separated, no trailing slashes |
| DEBUG | Debug mode flag | False | Set to True only in development |
| ENVIRONMENT | Environment name | development | development, staging, or production |
| LOG_LEVEL | Logging verbosity | INFO | DEBUG, INFO, WARNING, ERROR, CRITICAL |
| SERVER_HOST | Server bind address | 0.0.0.0 | 0.0.0.0 = all interfaces, 127.0.0.1 = localhost only |
| SERVER_PORT | Server port | 8000 | Common ports: 8000, 3000, 5000 |

---

## Troubleshooting

### Error: "connection refused" or "could not connect to server"

**Causes**:
- PostgreSQL not running
- Wrong host/port
- Firewall blocking connection

**Solutions**:
```bash
# Check if PostgreSQL is running
docker ps  # If using Docker
psql -h localhost -U postgres  # If using local PostgreSQL

# Check port
netstat -an | grep 5432  # Windows
lsof -i :5432  # macOS/Linux

# Start PostgreSQL
docker start hackathon-postgres  # Docker
brew services start postgresql@14  # macOS
sudo service postgresql start  # Linux
```

### Error: "database does not exist"

**Cause**: hackathon_todo database not created

**Solution**:
```bash
# Create database
psql -h localhost -U postgres -c "CREATE DATABASE hackathon_todo;"

# Verify
psql -h localhost -U postgres -l | grep hackathon_todo
```

### Error: "password authentication failed"

**Cause**: Wrong username/password

**Solution**:
```bash
# Check .env file has correct credentials
cat backend/.env | grep DATABASE_URL

# Test with correct credentials
psql -h localhost -U postgres -W  # Will prompt for password
```

### Error: "user 'postgres' does not exist"

**Cause**: PostgreSQL installation incomplete or user deleted

**Solution**:
```bash
# Recreate postgres user (requires superuser access)
sudo -u postgres createuser postgres -s -P

# Or reinstall PostgreSQL
```

### Error: "pydantic_core._pydantic_core.ValidationError"

**Cause**: Settings validation failed (likely DATABASE_URL or JWT_SECRET_KEY)

**Solution**:
```bash
# Ensure .env file is in backend directory
cd backend
cp .env.development .env

# Verify DATABASE_URL format
# Should be: postgresql://username:password@host:port/database

# Ensure JWT_SECRET_KEY is at least 32 characters
```

### Error: "could not translate host name 'postgres' to address"

**Cause**: Using Docker host name 'postgres' without Docker network

**Solution**:
```bash
# If running backend outside Docker, change DATABASE_URL to:
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/hackathon_todo

# If all running in Docker, service name 'postgres' works (docker-compose handles it)
```

---

## Performance Optimization

### Connection Pool Configuration

Backend uses connection pooling for performance:

```python
# src/app/database.py
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    poolclass=QueuePool,
    pool_size=5,           # Number of connections to keep open
    max_overflow=10,       # Extra connections if pool is full
    pool_pre_ping=True,    # Test connections before using
)
```

**Tuning**:
- Increase `pool_size` if you have many concurrent users
- Increase `max_overflow` if you expect traffic spikes
- Keep `pool_pre_ping=True` to prevent stale connections

### Query Performance

#### Indexes
Database has indexes on frequently queried columns:

```sql
-- User lookups
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- Task filtering
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);

-- Token lookup
CREATE INDEX idx_refresh_token_token ON refresh_token(token);
```

#### Slow Query Monitoring
```bash
# Enable slow query logging (PostgreSQL)
psql -h localhost -U postgres -d hackathon_todo

ALTER SYSTEM SET log_min_duration_statement = 1000;  -- Log queries > 1000ms
SELECT pg_reload_conf();

# View logs
tail -f /var/lib/postgresql/data/log/*
```

### Memory Usage

Monitor PostgreSQL memory:

```bash
# Check shared memory
psql -h localhost -U postgres -c "SHOW shared_buffers;"

# Adjust if needed (requires restart)
psql -h localhost -U postgres -c "ALTER SYSTEM SET shared_buffers = '256MB';"
```

---

## Migration Strategy (Future)

When database schema needs to change, use **Alembic** for migrations:

```bash
# Initialize Alembic (one-time)
cd backend
alembic init migrations

# Create a migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

For now, SQLModel handles schema creation automatically.

---

## Security Considerations

### Database Access

**Development** (localhost only):
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost/hackathon_todo
```

**Production** (should be):
- Use strong, random passwords
- Restrict PostgreSQL to application servers only
- Use SSL/TLS for connections
- Enable PostgreSQL authentication logs
- Regular backups with encryption

### Credentials Management

**Development**:
```bash
# Use .env.development with dev credentials
# File is in .gitignore - never commit
DATABASE_URL=postgresql://postgres:postgres@localhost/hackathon_todo
```

**Production**:
```bash
# Use environment variables or secrets management
# Never commit production credentials
# Use services like AWS Secrets Manager, HashiCorp Vault, etc.
export DATABASE_URL=postgresql://prod_user:strong_password@prod_host:5432/hackathon_todo
```

### Backup Security

```bash
# Encrypt backups
pg_dump postgresql://user:pass@host/db | gzip | openssl enc -aes-256-cbc -out backup.sql.gz.enc

# Decrypt and restore
openssl enc -d -aes-256-cbc -in backup.sql.gz.enc | gunzip | psql postgresql://user:pass@host/db
```

---

## Testing Database Setup

### Test Script

Create `test_database.py`:

```python
#!/usr/bin/env python3
"""Test database connectivity and schema."""

from sqlalchemy import text
from src.app.database import engine
from src.app.config import settings

def test_connection():
    """Test basic database connection."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✓ Database connection successful")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def test_tables():
    """Verify required tables exist."""
    required_tables = ['users', 'tasks', 'refresh_token']

    try:
        with engine.connect() as connection:
            for table in required_tables:
                result = connection.execute(
                    text(f"SELECT to_regclass('public.{table}')")
                )
                exists = result.scalar() is not None
                status = "✓" if exists else "✗"
                print(f"{status} Table '{table}' exists: {exists}")
            return True
    except Exception as e:
        print(f"✗ Table check failed: {e}")
        return False

def test_indexes():
    """Verify indexes exist."""
    expected_indexes = {
        'users': ['idx_users_email', 'idx_users_username'],
        'tasks': ['idx_tasks_user_id', 'idx_tasks_status', 'idx_tasks_due_date'],
    }

    try:
        with engine.connect() as connection:
            for table, indexes in expected_indexes.items():
                for index in indexes:
                    result = connection.execute(
                        text(f"SELECT indexname FROM pg_indexes WHERE indexname = '{index}'")
                    )
                    exists = result.scalar() is not None
                    status = "✓" if exists else "⚠"
                    print(f"{status} Index '{index}' exists: {exists}")
        return True
    except Exception as e:
        print(f"⚠ Index check failed (non-critical): {e}")
        return True

if __name__ == '__main__':
    print("Testing Database Setup")
    print("=" * 50)
    print(f"DATABASE_URL: {settings.DATABASE_URL}")
    print()

    tests = [
        ("Connection", test_connection),
        ("Tables", test_tables),
        ("Indexes", test_indexes),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 50)
        results.append(test_func())

    print("\n" + "=" * 50)
    if all(results):
        print("✓ All database tests passed!")
    else:
        print("✗ Some database tests failed. See above for details.")
```

Run:
```bash
cd backend
python test_database.py
```

---

## Quick Reference

### Common Commands

```bash
# Start PostgreSQL (Docker)
docker start hackathon-postgres

# Stop PostgreSQL
docker stop hackathon-postgres

# Connect with psql
psql -h localhost -U postgres -d hackathon_todo

# List all databases
\l

# Connect to database
\c hackathon_todo

# List all tables
\dt

# Describe table structure
\d users

# Count records
SELECT COUNT(*) FROM users;

# Exit psql
\q
```

### Environment Setup Checklist

- [ ] PostgreSQL 14+ installed and running
- [ ] hackathon_todo database created
- [ ] Tables created (automatic on backend startup)
- [ ] Backend environment variables configured
- [ ] Database connection tested
- [ ] Backend imports verified
- [ ] Backend starts without errors

---

## Next Steps

1. **Choose Setup Method**: Docker (recommended) or Local PostgreSQL
2. **Start Database**: Use appropriate startup command for your method
3. **Verify Connection**: Run test commands from "Connection Verification" section
4. **Start Backend**: `uvicorn src.app.main:app --reload`
5. **Test API**: Access http://localhost:8000/api/docs
6. **Create Test User**: Register via signup endpoint
7. **Test CRUD**: Create, read, update, delete tasks

---

## Support

If you encounter issues:

1. Check the **Troubleshooting** section above
2. Verify PostgreSQL is running: `docker ps` or `psql -U postgres`
3. Check DATABASE_URL format in .env
4. Review backend logs: `uvicorn src.app.main:app --reload`
5. Test connection manually: `psql -h localhost -U postgres -d hackathon_todo`

---

**Last Updated**: December 30, 2025
**PostgreSQL Version**: 14+
**Connection**: PostgreSQL protocol on port 5432

