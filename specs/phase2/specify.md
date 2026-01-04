# Phase 2: Core Backend API Development - Specification

## API Specification

### Base URL
- Development: `http://localhost:3000/api/v1`
- Production: `https://api.hackathon-todo.com/api/v1`

### Authentication
- **Type**: Bearer Token (JWT)
- **Header**: `Authorization: Bearer <token>`
- **Token Expiry**: 24 hours
- **Refresh Token**: 7 days

## Endpoint Specifications

### Authentication Endpoints

#### POST /auth/register
Register a new user account
```
Request:
{
  "email": "user@example.com",
  "password": "securePassword123!",
  "name": "John Doe"
}

Response (201):
{
  "success": true,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2024-01-01T00:00:00Z"
  },
  "token": "jwt_token",
  "refreshToken": "refresh_token"
}

Errors:
- 400: Invalid input
- 409: Email already registered
- 500: Server error
```

#### POST /auth/login
User login with email and password
```
Request:
{
  "email": "user@example.com",
  "password": "securePassword123!"
}

Response (200):
{
  "success": true,
  "user": { ... },
  "token": "jwt_token",
  "refreshToken": "refresh_token"
}

Errors:
- 400: Invalid credentials
- 401: Unauthorized
- 500: Server error
```

#### POST /auth/refresh
Refresh JWT token using refresh token
```
Request:
{
  "refreshToken": "refresh_token"
}

Response (200):
{
  "success": true,
  "token": "new_jwt_token",
  "refreshToken": "new_refresh_token"
}

Errors:
- 401: Invalid refresh token
- 500: Server error
```

#### POST /auth/logout
Logout user (client-side token removal)
```
Response (200):
{
  "success": true,
  "message": "Logged out successfully"
}
```

### User Endpoints

#### GET /users/:id
Get user profile information
```
Headers: Authorization: Bearer <token>

Response (200):
{
  "success": true,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "avatar": "url",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}

Errors:
- 401: Unauthorized
- 404: User not found
- 500: Server error
```

#### PUT /users/:id
Update user profile
```
Headers: Authorization: Bearer <token>

Request:
{
  "name": "Jane Doe",
  "avatar": "url"
}

Response (200):
{
  "success": true,
  "user": { ... }
}

Errors:
- 400: Invalid input
- 401: Unauthorized
- 403: Forbidden (cannot edit other users)
- 404: User not found
```

#### PUT /users/:id/password
Change user password
```
Headers: Authorization: Bearer <token>

Request:
{
  "oldPassword": "oldPassword123!",
  "newPassword": "newPassword123!"
}

Response (200):
{
  "success": true,
  "message": "Password updated successfully"
}

Errors:
- 400: Invalid password
- 401: Unauthorized/Invalid old password
- 500: Server error
```

### Todo Endpoints

#### GET /todos
List all todos for authenticated user
```
Headers: Authorization: Bearer <token>

Query Parameters:
- status: "pending" | "completed" | "archived"
- priority: "low" | "medium" | "high"
- sortBy: "due_date" | "created_at" | "priority"
- order: "asc" | "desc"
- page: number (default: 1)
- limit: number (default: 20)

Response (200):
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "title": "Complete project",
      "description": "Finish the hackathon project",
      "status": "pending",
      "priority": "high",
      "due_date": "2024-12-31T00:00:00Z",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 50,
    "pages": 3
  }
}

Errors:
- 401: Unauthorized
- 500: Server error
```

#### POST /todos
Create a new todo
```
Headers: Authorization: Bearer <token>

Request:
{
  "title": "Complete project",
  "description": "Finish the hackathon project",
  "priority": "high",
  "due_date": "2024-12-31T00:00:00Z"
}

Response (201):
{
  "success": true,
  "data": { ... }
}

Errors:
- 400: Invalid input
- 401: Unauthorized
- 500: Server error
```

#### GET /todos/:id
Get specific todo details
```
Headers: Authorization: Bearer <token>

Response (200):
{
  "success": true,
  "data": { ... }
}

Errors:
- 401: Unauthorized
- 404: Todo not found
- 500: Server error
```

#### PUT /todos/:id
Update a todo
```
Headers: Authorization: Bearer <token>

Request:
{
  "title": "Updated title",
  "status": "completed",
  "priority": "medium"
}

Response (200):
{
  "success": true,
  "data": { ... }
}

Errors:
- 400: Invalid input
- 401: Unauthorized
- 403: Forbidden
- 404: Todo not found
```

#### DELETE /todos/:id
Delete a todo
```
Headers: Authorization: Bearer <token>

Response (200):
{
  "success": true,
  "message": "Todo deleted successfully"
}

Errors:
- 401: Unauthorized
- 403: Forbidden
- 404: Todo not found
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  avatar VARCHAR(500),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_active BOOLEAN DEFAULT true
);

CREATE INDEX idx_users_email ON users(email);
```

### Todos Table
```sql
CREATE TABLE todos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'archived')),
  priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high')),
  due_date TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_status ON todos(status);
CREATE INDEX idx_todos_due_date ON todos(due_date);
```

### Refresh Tokens Table
```sql
CREATE TABLE refresh_tokens (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token VARCHAR(500) NOT NULL UNIQUE,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_expires_at ON refresh_tokens(expires_at);
```

## Error Response Format

### Standard Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {}
  }
}
```

### Validation Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "field_name": ["Error message 1", "Error message 2"]
    }
  }
}
```

## Validation Rules

### User Email
- Must be valid email format
- Must be unique in database
- Required field

### User Password
- Minimum 8 characters
- Must contain uppercase letter
- Must contain lowercase letter
- Must contain number
- Must contain special character

### Todo Title
- Required field
- Minimum 3 characters
- Maximum 255 characters

### Todo Priority
- Enum: low, medium, high
- Default: medium

### Todo Status
- Enum: pending, completed, archived
- Default: pending

## Security Requirements

1. **Password Hashing**: bcrypt with salt rounds 10
2. **JWT Signing**: HS256 or RS256
3. **CORS**: Configured for frontend domain
4. **Rate Limiting**: 100 requests per 15 minutes per IP
5. **Input Validation**: All inputs validated server-side
6. **SQL Injection Prevention**: Use parameterized queries
7. **HTTPS**: Required in production
8. **CSRF Protection**: SameSite cookie attribute

## Testing Requirements

- Unit tests for all services
- Integration tests for API endpoints
- Database migration tests
- Authentication flow tests
- Minimum 80% code coverage
