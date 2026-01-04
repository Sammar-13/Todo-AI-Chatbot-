# Phase II Specifications: Multi-User Web Todo Application

## Document Overview

**Phase**: Phase II (Web Application)
**Title**: Convert CLI Todo into Multi-User Web Application
**Stack**: Next.js (Frontend) + FastAPI (Backend) + PostgreSQL (Database)
**Status**: SPECIFICATION PHASE
**Date**: December 30, 2025

---

## 1. Executive Summary

Phase II transforms the Phase I single-user CLI Todo application into a modern, scalable multi-user web application with:

- **Frontend**: Next.js 14+ with App Router, TypeScript, Tailwind CSS
- **Backend**: FastAPI with SQLModel ORM
- **Database**: Neon PostgreSQL with SQLAlchemy migrations
- **Authentication**: JWT-based auth with refresh tokens
- **Architecture**: RESTful API with separation of concerns

### Key Additions from Phase I
- Multi-user support with authentication
- Persistent database storage
- Web-based UI/UX
- Real-time responsiveness
- User session management
- Task sharing capabilities (Phase II+)

---

## 2. Technology Stack Details

### Frontend (Next.js)
- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context API (or TanStack Query for server state)
- **HTTP Client**: Fetch API with custom hooks or axios
- **Validation**: Zod for runtime validation
- **Form Handling**: React Hook Form

### Backend (FastAPI)
- **Framework**: FastAPI 0.100+
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: Neon PostgreSQL
- **Authentication**: PyJWT, passlib, python-jose
- **Validation**: Pydantic v2
- **CORS**: fastapi-cors
- **Migrations**: Alembic

### Database (PostgreSQL)
- **Hosting**: Neon (PostgreSQL 14+)
- **Connection**: psycopg2 or asyncpg
- **ORM**: SQLModel
- **Migrations**: Alembic with auto-migration support

---

## 3. System Architecture

### 3.1 High-Level Architecture

```
┌─────────────────────────┐
│   Next.js Frontend      │
│  (React + TypeScript)   │
└──────────────┬──────────┘
               │ (HTTPS)
               │ REST API
               │
┌──────────────▼──────────┐
│   FastAPI Backend       │
│  (Python + SQLModel)    │
└──────────────┬──────────┘
               │
               │ (TCP)
               │
┌──────────────▼──────────┐
│  Neon PostgreSQL        │
│  (Cloud Database)       │
└─────────────────────────┘
```

### 3.2 Request/Response Flow

```
User Browser
    │
    ├─ Request: GET /api/auth/login
    │ Response: { access_token, refresh_token, user }
    │
    ├─ Request: GET /api/tasks (with JWT header)
    │ Response: [ Task, Task, ... ]
    │
    └─ Request: POST /api/tasks (with body + JWT)
      Response: { id, title, status, created_at, ... }
```

### 3.3 Authentication Flow

```
1. User enters credentials
   └─→ POST /api/auth/signup or /api/auth/login
       │
       └─→ Backend validates credentials
           │
           └─→ Generate JWT tokens
               │
               └─→ Return: {
                     access_token (15min exp),
                     refresh_token (7day exp),
                     user: { id, email, name }
                   }

2. Client stores tokens (localStorage or httpOnly cookies)
   └─→ Include access_token in Authorization header for API requests

3. If access_token expires
   └─→ POST /api/auth/refresh with refresh_token
       │
       └─→ Backend validates refresh_token
           │
           └─→ Return: { access_token, refresh_token }

4. Logout
   └─→ POST /api/auth/logout
       │
       └─→ Clear tokens on client
```

---

## 4. Database Schema

### 4.1 Tables Overview

```
users
├── id (UUID, PK)
├── email (VARCHAR, UNIQUE)
├── username (VARCHAR, UNIQUE)
├── password_hash (VARCHAR)
├── full_name (VARCHAR)
├── avatar_url (VARCHAR, NULL)
├── is_active (BOOLEAN)
├── created_at (TIMESTAMP)
├── updated_at (TIMESTAMP)

tasks
├── id (UUID, PK)
├── user_id (UUID, FK → users.id)
├── title (VARCHAR)
├── description (TEXT)
├── status (VARCHAR) ['pending', 'completed']
├── priority (VARCHAR) ['low', 'medium', 'high']
├── due_date (DATE, NULL)
├── created_at (TIMESTAMP)
├── updated_at (TIMESTAMP)
├── completed_at (TIMESTAMP, NULL)

task_shares (future)
├── id (UUID, PK)
├── task_id (UUID, FK → tasks.id)
├── shared_with_user_id (UUID, FK → users.id)
├── permission (VARCHAR) ['view', 'edit']
├── created_at (TIMESTAMP)

refresh_tokens (optional)
├── id (UUID, PK)
├── user_id (UUID, FK → users.id)
├── token (VARCHAR, UNIQUE)
├── expires_at (TIMESTAMP)
├── created_at (TIMESTAMP)
```

### 4.2 Table Specifications

#### Users Table
- **Purpose**: Store user account information
- **Uniqueness**: email and username must be unique
- **Password**: Stored as bcrypt hash (min 12 rounds)
- **Timestamps**: All records have created_at and updated_at
- **Soft Delete**: is_active flag (no hard delete)

#### Tasks Table
- **Purpose**: Store user tasks
- **Ownership**: user_id links each task to owner
- **Status**: Enum ['pending', 'completed']
- **Priority**: New field (low/medium/high) - enhancement from Phase I
- **Timestamps**: created_at, updated_at, completed_at (NULL until completion)
- **Soft Delete**: Could use is_deleted flag (optional)

#### Task_Shares Table (Phase II+)
- **Purpose**: Enable task sharing between users
- **Permission**: view (read-only) or edit (read-write)
- **Scope**: Out of scope for Phase II, prepared for future

#### Refresh_Tokens Table (Optional)
- **Purpose**: Track issued refresh tokens for revocation
- **Blacklist**: Prevent use of revoked tokens
- **Scope**: Optional optimization, simpler approach: just verify signature

---

## 5. REST API Specification

### 5.1 Base Configuration
- **Base URL**: `https://api.example.com` (development: `http://localhost:8000`)
- **API Version**: `/api/v1` or `/api`
- **Authentication**: Bearer JWT in Authorization header
- **Content-Type**: application/json
- **Rate Limiting**: Optional (TBD)

### 5.2 Authentication Endpoints

#### 5.2.1 POST /api/auth/signup
Create new user account

**Request**:
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "password": "securePassword123!"
}
```

**Validation**:
- email: valid email format, unique, max 255 chars
- username: alphanumeric + underscore, unique, 3-20 chars
- full_name: non-empty, max 255 chars
- password: min 8 chars, at least 1 uppercase, 1 lowercase, 1 digit, 1 special char

**Response** (201):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "avatar_url": null,
    "created_at": "2025-12-30T10:00:00Z"
  },
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

**Error Responses**:
- 400: Validation error (invalid email, weak password, etc.)
- 409: Email or username already exists

#### 5.2.2 POST /api/auth/login
Authenticate user and get tokens

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123!"
}
```

**Validation**:
- email: valid format
- password: non-empty

**Response** (200):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "avatar_url": null,
    "created_at": "2025-12-30T10:00:00Z"
  },
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

**Error Responses**:
- 401: Invalid credentials
- 400: Validation error

#### 5.2.3 POST /api/auth/refresh
Refresh access token using refresh token

**Request**:
```json
{
  "refresh_token": "eyJhbGc..."
}
```

**Response** (200):
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

**Error Responses**:
- 401: Invalid or expired refresh token

#### 5.2.4 POST /api/auth/logout
Invalidate user session

**Request**:
```
Header: Authorization: Bearer {access_token}
```

**Response** (200):
```json
{
  "message": "Logged out successfully"
}
```

#### 5.2.5 GET /api/auth/me
Get current authenticated user info

**Request**:
```
Header: Authorization: Bearer {access_token}
```

**Response** (200):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "avatar_url": null,
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:00Z"
}
```

**Error Responses**:
- 401: No token or invalid token

### 5.3 Task Endpoints

#### 5.3.1 GET /api/tasks
List all tasks for authenticated user with optional filtering

**Request**:
```
Header: Authorization: Bearer {access_token}
Query Parameters:
  - status: 'pending' | 'completed' (optional)
  - priority: 'low' | 'medium' | 'high' (optional)
  - sort: 'created_at' | 'due_date' | 'priority' (optional, default: created_at)
  - order: 'asc' | 'desc' (optional, default: desc)
  - skip: number (optional, default: 0)
  - limit: number (optional, default: 100, max: 500)
```

**Response** (200):
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "user_id": "660e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "status": "pending",
      "priority": "high",
      "due_date": "2025-12-31",
      "created_at": "2025-12-30T10:00:00Z",
      "updated_at": "2025-12-30T10:00:00Z",
      "completed_at": null
    }
  ],
  "total": 42,
  "skip": 0,
  "limit": 100
}
```

**Error Responses**:
- 401: Not authenticated

#### 5.3.2 POST /api/tasks
Create new task

**Request**:
```
Header: Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "high",
  "due_date": "2025-12-31"
}
```

**Validation**:
- title: required, 1-255 chars
- description: optional, max 1000 chars
- priority: optional, enum ['low', 'medium', 'high'], default 'medium'
- due_date: optional, ISO date format, must be >= today

**Response** (201):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "660e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending",
  "priority": "high",
  "due_date": "2025-12-31",
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:00Z",
  "completed_at": null
}
```

**Error Responses**:
- 400: Validation error
- 401: Not authenticated

#### 5.3.3 GET /api/tasks/{task_id}
Get single task details

**Request**:
```
Header: Authorization: Bearer {access_token}
```

**Response** (200):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "660e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending",
  "priority": "high",
  "due_date": "2025-12-31",
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:00Z",
  "completed_at": null
}
```

**Error Responses**:
- 401: Not authenticated
- 403: Task belongs to different user
- 404: Task not found

#### 5.3.4 PATCH /api/tasks/{task_id}
Update task (partial update)

**Request**:
```
Header: Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Buy groceries and cook",
  "priority": "medium",
  "due_date": "2026-01-02"
}
```

**Validation**:
- All fields optional
- Same constraints as POST /api/tasks

**Response** (200):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "660e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries and cook",
  "description": "Milk, eggs, bread",
  "status": "pending",
  "priority": "medium",
  "due_date": "2026-01-02",
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:30Z",
  "completed_at": null
}
```

**Error Responses**:
- 400: Validation error
- 401: Not authenticated
- 403: Not authorized to update
- 404: Task not found

#### 5.3.5 PATCH /api/tasks/{task_id}/status
Update only task status

**Request**:
```
Header: Authorization: Bearer {access_token}
Content-Type: application/json

{
  "status": "completed"
}
```

**Validation**:
- status: required, enum ['pending', 'completed']

**Response** (200):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "660e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "completed",
  "priority": "high",
  "due_date": "2025-12-31",
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T11:00:00Z",
  "completed_at": "2025-12-30T11:00:00Z"
}
```

**Error Responses**:
- 400: Invalid status
- 401: Not authenticated
- 403: Not authorized
- 404: Task not found

#### 5.3.6 DELETE /api/tasks/{task_id}
Delete task

**Request**:
```
Header: Authorization: Bearer {access_token}
```

**Response** (204): No content

**Error Responses**:
- 401: Not authenticated
- 403: Not authorized
- 404: Task not found

### 5.4 User Profile Endpoints (Optional Phase II+)

#### 5.4.1 GET /api/users/profile
Get current user profile

**Response** (200):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "avatar_url": "https://...",
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:00Z"
}
```

#### 5.4.2 PATCH /api/users/profile
Update user profile

**Request**:
```json
{
  "full_name": "John Doe Jr",
  "avatar_url": "https://..."
}
```

**Response** (200): Updated user object

---

## 6. Frontend Pages and Routes

### 6.1 Page Structure (Next.js App Router)

```
app/
├── layout.tsx                    # Root layout
├── page.tsx                      # Landing/home page
├── (auth)/
│   ├── layout.tsx               # Auth layout (no sidebar)
│   ├── login/
│   │   └── page.tsx             # Login page
│   ├── signup/
│   │   └── page.tsx             # Sign up page
│   └── forgot-password/
│       └── page.tsx             # Forgot password (Phase II+)
├── (dashboard)/
│   ├── layout.tsx               # Dashboard layout (with sidebar)
│   ├── page.tsx                 # Dashboard/tasks list
│   ├── tasks/
│   │   ├── page.tsx             # Tasks overview
│   │   └── [id]/
│   │       └── page.tsx         # Task detail page
│   ├── settings/
│   │   └── page.tsx             # User settings
│   └── profile/
│       └── page.tsx             # User profile
└── api/
    ├── auth/
    │   ├── login/route.ts       # Proxy to backend
    │   ├── signup/route.ts
    │   ├── logout/route.ts
    │   └── refresh/route.ts
    └── tasks/
        └── route.ts             # Proxy to backend
```

### 6.2 Page Specifications

#### 6.2.1 Public Pages

**Landing Page (/)** - Not authenticated
- Hero section with app description
- Call-to-action buttons: "Sign Up" / "Log In"
- Feature highlights
- Footer with links

**Login Page (/login)** - Not authenticated
- Email input field
- Password input field
- "Remember me" checkbox
- Login button
- Link to sign up page
- Link to forgot password (optional)
- Error messages display
- Loading state during submission

**Sign Up Page (/signup)** - Not authenticated
- Email input field
- Username input field
- Full name input field
- Password input field with strength indicator
- Confirm password field
- Terms & conditions checkbox
- Sign up button
- Link to login page
- Field validation messages
- Loading state

#### 6.2.2 Authenticated Pages (Dashboard Layout)

**Layout Components**:
- Navigation bar: logo, user menu, logout button
- Sidebar: navigation links
- Main content area
- Optional: mobile hamburger menu

**Tasks List Page (/tasks or /dashboard)** - Authenticated
- **Header**:
  - Search/filter box (status, priority, due date)
  - "Create Task" button
  - View toggle (list/grid)

- **Task List Display**:
  - Task card with:
    - Title (clickable → detail page)
    - Description (truncated)
    - Status badge (pending/completed)
    - Priority badge (low/medium/high)
    - Due date (if set)
    - Quick action buttons: complete/edit/delete

  - Empty state: "No tasks yet. Create one to get started!"
  - Loading skeleton while fetching
  - Pagination or infinite scroll
  - Statistics: "X pending, Y completed"

**Task Detail Page (/tasks/[id])** - Authenticated
- **Header**: Title with edit button
- **Content**:
  - Full description (editable)
  - Status selector dropdown
  - Priority selector
  - Due date picker
  - Created/Updated timestamps
  - Completion time (if completed)

- **Actions**:
  - Save button (appears when modified)
  - Mark as complete/pending toggle
  - Delete button with confirmation
  - Back to list link

- **Error State**: "Task not found" or "No access"

**Settings Page (/settings)** - Authenticated
- **Profile Section**:
  - Avatar upload
  - Full name input
  - Email display (read-only)
  - Username display (read-only)

- **Account Section**:
  - Change password form
  - Email notifications toggle
  - Theme preference (light/dark)

- **Danger Zone**:
  - Delete account button with confirmation

**Profile Page (/profile)** - Authenticated
- User information display
- Statistics: task count, completion rate
- Recent activity

---

## 7. Frontend Components and Features

### 7.1 Key Components

- **TaskForm**: Create/edit task
- **TaskCard**: Display task in list
- **TaskDetail**: Full task view
- **TaskFilter**: Filter and search
- **AuthForm**: Login/signup form
- **UserMenu**: User dropdown menu
- **Navigation**: Sidebar/navbar
- **Modal**: Confirmation dialogs
- **Toast**: Notification messages
- **Skeleton**: Loading placeholders

### 7.2 State Management

**Global State (Context API)**:
- `AuthContext`: Current user, tokens, login/logout
- `TaskContext`: Tasks list, current task, loading states
- `UIContext`: Theme, sidebar open/close, notifications

**Local State (Component)**:
- Form inputs and validation
- Modal visibility
- Loading states

### 7.3 Features

**Authentication**:
- Sign up with validation
- Login with remember-me
- Token refresh on expiration
- Logout with cleanup
- Protected routes
- Redirect on unauthorized access

**Task Management**:
- Create task with validation
- List tasks with infinite scroll
- Filter by status/priority
- Search by title
- Edit task details
- Mark complete/pending
- Delete with confirmation
- Sort by various fields

**UI/UX**:
- Responsive design (mobile-first)
- Dark mode support
- Loading indicators
- Error boundaries
- Toast notifications
- Form validation messages
- Accessibility (WCAG 2.1 AA)

---

## 8. Authentication Details

### 8.1 JWT Token Structure

**Access Token** (expires in 15 minutes):
```
Header:
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload:
{
  "sub": "user_id_here",
  "email": "user@example.com",
  "username": "johndoe",
  "iat": 1703944800,
  "exp": 1703945700
}
```

**Refresh Token** (expires in 7 days):
```
Payload:
{
  "sub": "user_id_here",
  "type": "refresh",
  "iat": 1703944800,
  "exp": 1704549600
}
```

### 8.2 Password Security

- **Hashing**: bcrypt with 12+ rounds
- **Validation**: Min 8 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char
- **Storage**: Hash only, never plain text
- **Transmission**: HTTPS only

### 8.3 Token Storage

**Frontend**:
- **access_token**: localStorage (simpler) or httpOnly cookie (more secure)
- **refresh_token**: localStorage or httpOnly cookie
- Alternative: Store only in memory (most secure, requires refresh on page load)

**Backend**:
- Validate JWT signature using secret key
- Check token expiration
- Extract user_id from token claims

---

## 9. Error Handling

### 9.1 HTTP Status Codes

- **200**: OK - Request successful
- **201**: Created - Resource created
- **204**: No Content - Successful deletion
- **400**: Bad Request - Validation error
- **401**: Unauthorized - Missing/invalid auth
- **403**: Forbidden - Not authorized for resource
- **404**: Not Found - Resource doesn't exist
- **409**: Conflict - Email/username already exists
- **422**: Unprocessable Entity - Validation failure
- **500**: Internal Server Error - Server error
- **503**: Service Unavailable - Maintenance

### 9.2 Error Response Format

```json
{
  "detail": "Invalid credentials",
  "error_code": "INVALID_CREDENTIALS",
  "status": 401,
  "timestamp": "2025-12-30T10:00:00Z"
}
```

For validation errors:
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    },
    {
      "field": "password",
      "message": "Password too short"
    }
  ],
  "status": 422
}
```

---

## 10. Security Considerations

### 10.1 Frontend Security
- **HTTPS Only**: All API calls over HTTPS
- **XSS Prevention**: Sanitize user input, use DOMPurify
- **CSRF Protection**: Use SameSite cookies
- **Token Storage**: Secure storage mechanism
- **Input Validation**: Client-side validation (not sufficient alone)
- **Dependency Scanning**: Regular npm audit

### 10.2 Backend Security
- **HTTPS Only**: Enforce TLS 1.2+
- **CORS**: Configure allowed origins
- **Rate Limiting**: Prevent brute force attacks
- **Input Validation**: Pydantic validation on all endpoints
- **SQL Injection**: Use SQLModel/SQLAlchemy parameterized queries
- **Password Hashing**: bcrypt with adequate rounds
- **Secrets Management**: Use environment variables for JWT secret
- **Dependency Scanning**: Regular pip audit

### 10.3 Database Security
- **Encryption at Rest**: PostgreSQL encryption (optional)
- **Encryption in Transit**: SSL/TLS connections
- **Access Control**: Strong database credentials
- **Backups**: Regular backups with Neon
- **Monitoring**: Track access patterns

---

## 11. Performance Considerations

### 11.1 Frontend
- **Code Splitting**: Lazy load pages with Next.js
- **Image Optimization**: Use Next.js Image component
- **Caching**: HTTP caching headers
- **Bundle Analysis**: Monitor bundle size
- **Core Web Vitals**: Optimize LCP, FID, CLS

### 11.2 Backend
- **Database Indexing**: Index on user_id, task.user_id
- **Query Optimization**: Use pagination, limit results
- **Caching**: Redis for session storage (optional)
- **Connection Pooling**: Use SQLAlchemy connection pools
- **Async Operations**: Use async/await in FastAPI

### 11.3 Database
- **Indexes**:
  - PRIMARY: id
  - FOREIGN: user_id on tasks table
  - COMPOSITE: (user_id, status) for filtering
- **Query Performance**: Explain plans for slow queries
- **Connection Limits**: Configure Neon connection limits

---

## 12. Testing Strategy

### 12.1 Frontend Testing
- **Unit Tests**: React components (Jest + React Testing Library)
- **Integration Tests**: API interaction flows
- **E2E Tests**: Full user workflows (Cypress or Playwright)
- **Coverage Target**: >80% for critical paths

### 12.2 Backend Testing
- **Unit Tests**: Models, validators, utilities
- **Integration Tests**: API endpoints with test database
- **E2E Tests**: Full request/response cycles
- **Coverage Target**: >85% for API endpoints

### 12.3 Test Data
- **Fixtures**: Sample users, tasks for testing
- **Database**: Separate test database (Neon branch or local)
- **Cleanup**: Reset database between test runs

---

## 13. Deployment Strategy

### 13.1 Frontend Deployment
- **Hosting**: Vercel (Next.js native)
- **Environment**: Development, Staging, Production
- **CI/CD**: GitHub Actions → Vercel
- **Build**: Next.js build optimization
- **Monitoring**: Vercel Analytics

### 13.2 Backend Deployment
- **Hosting**: Railway, Heroku, or AWS Elastic Beanstalk
- **Environment**: Development, Staging, Production
- **CI/CD**: GitHub Actions → Container Registry → Host
- **Database**: Neon PostgreSQL (managed)
- **Monitoring**: Logging, error tracking (Sentry)

### 13.3 Environment Configuration
```
Development:
  - Frontend: http://localhost:3000
  - Backend: http://localhost:8000
  - Database: localhost PostgreSQL or Neon dev branch

Staging:
  - Frontend: staging-app.example.com
  - Backend: api-staging.example.com
  - Database: Neon staging branch

Production:
  - Frontend: app.example.com (Vercel)
  - Backend: api.example.com
  - Database: Neon production
```

---

## 14. Acceptance Criteria

### 14.1 Authentication
- [ ] User can sign up with email validation
- [ ] User can log in with email/password
- [ ] JWT tokens are generated correctly
- [ ] Access token expires in 15 minutes
- [ ] Refresh token refreshes access token
- [ ] User can log out and tokens are invalidated
- [ ] Protected routes redirect to login
- [ ] Invalid credentials return 401

### 14.2 Task Management
- [ ] Authenticated user can create task
- [ ] User can list all their tasks
- [ ] User can view task details
- [ ] User can edit task (all fields)
- [ ] User can mark task as completed
- [ ] User can delete task
- [ ] Task list can be filtered by status
- [ ] Task list can be filtered by priority
- [ ] Tasks are sorted by created_at by default
- [ ] User cannot access other user's tasks

### 14.3 Frontend
- [ ] Landing page displays correctly
- [ ] Login form validates input
- [ ] Sign up form validates input and password strength
- [ ] Task list displays all user tasks
- [ ] Task list is responsive (mobile/tablet/desktop)
- [ ] Create task modal appears and works
- [ ] Edit task modal appears and works
- [ ] Delete confirmation modal appears
- [ ] Loading states display correctly
- [ ] Error messages display clearly
- [ ] User menu shows current user
- [ ] Logout clears tokens

### 14.4 Backend
- [ ] All endpoints return correct status codes
- [ ] All endpoints validate input
- [ ] All endpoints return correct error messages
- [ ] Database schema is correct
- [ ] Timestamps are set correctly
- [ ] User isolation is enforced
- [ ] Password is never returned in responses

### 14.5 Database
- [ ] PostgreSQL schema is created
- [ ] All tables have correct columns
- [ ] Foreign key constraints work
- [ ] Unique constraints on email/username
- [ ] Indexes are created for performance

---

## 15. Out of Scope (Future Phases)

- Task sharing between users
- Real-time collaboration
- Comments on tasks
- Task attachments
- Recurring tasks
- Calendar view
- Notifications
- Mobile native apps
- OAuth (Google/GitHub login)
- Two-factor authentication
- Team/workspace management
- Advanced analytics

---

## 16. Success Metrics

- [ ] All 30+ API endpoints working correctly
- [ ] User registration and login flow complete
- [ ] 100+ tasks can be created and managed
- [ ] Page loads in < 3 seconds
- [ ] API response time < 200ms
- [ ] >80% code coverage for critical paths
- [ ] Zero security vulnerabilities (OWASP)
- [ ] Accessible to WCAG 2.1 AA standard

---

## 17. Glossary

- **JWT**: JSON Web Token - stateless authentication
- **Access Token**: Short-lived token for API access
- **Refresh Token**: Long-lived token to get new access tokens
- **SQLModel**: Combines SQLAlchemy + Pydantic
- **Neon**: PostgreSQL database hosting service
- **CORS**: Cross-Origin Resource Sharing
- **WCAG**: Web Content Accessibility Guidelines

---

## 18. Document Metadata

**Document**: Phase II Specifications
**Version**: 1.0
**Status**: READY FOR ARCHITECTURE REVIEW
**Date**: December 30, 2025
**Last Updated**: December 30, 2025
**Author**: System Architect

**Approval Sign-Off**:
- [ ] Product Owner
- [ ] Technical Lead
- [ ] Security Officer

---

## Appendix A: API Endpoint Summary

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | /api/auth/signup | No | Create account |
| POST | /api/auth/login | No | Authenticate user |
| POST | /api/auth/refresh | No | Refresh token |
| POST | /api/auth/logout | Yes | End session |
| GET | /api/auth/me | Yes | Current user |
| GET | /api/tasks | Yes | List tasks |
| POST | /api/tasks | Yes | Create task |
| GET | /api/tasks/{id} | Yes | Task detail |
| PATCH | /api/tasks/{id} | Yes | Update task |
| PATCH | /api/tasks/{id}/status | Yes | Update status |
| DELETE | /api/tasks/{id} | Yes | Delete task |
| GET | /api/users/profile | Yes | User profile |
| PATCH | /api/users/profile | Yes | Update profile |

**Total: 13 endpoints (core Phase II)**

---

## Appendix B: Database Entity Relationships

```
users (1) ──────→ (many) tasks
  id                      user_id
  email                   title
  username                description
  password_hash           status
  full_name               priority
  avatar_url              due_date
  is_active               created_at
  created_at              updated_at
  updated_at              completed_at

(Future) task_shares
  id
  task_id (FK → tasks.id)
  shared_with_user_id (FK → users.id)
  permission
  created_at
```

---

## Appendix C: Environment Variables Template

**Backend (.env)**:
```
DATABASE_URL=postgresql://user:password@neon-host/dbname
JWT_SECRET=your-secret-key-here-min-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=["http://localhost:3000", "https://app.example.com"]
DEBUG=false
LOG_LEVEL=INFO
```

**Frontend (.env.local)**:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME=Todo App
```

---

## Appendix D: Technology Decision Matrix

| Decision | Option A | Option B | Chosen | Reason |
|----------|----------|----------|--------|--------|
| Frontend Framework | Vue.js | Next.js | Next.js | Built-in routing, SSR, Vercel integration |
| State Management | Redux | Context API | Context API | Simpler, adequate for Phase II scope |
| ORM | Django ORM | SQLModel | SQLModel | Pydantic integration, modern |
| Auth Method | OAuth | JWT | JWT | Simpler implementation, fine for Phase II |
| Database | Firebase | PostgreSQL | PostgreSQL | ACID compliance, relational schema |
| Token Storage | localStorage | httpOnly Cookie | localStorage | Simpler for Phase II, can upgrade |

---

**END OF SPECIFICATION**
