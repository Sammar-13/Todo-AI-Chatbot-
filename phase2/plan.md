# Phase II Architecture Plan: Full-Stack Multi-User Todo Application

## Document Overview

**Phase**: Phase II (Web Application Architecture)
**Title**: Full-Stack Architecture Plan for Multi-User Todo Application
**Scope**: System design, component responsibilities, integration points, data flows
**Status**: ARCHITECTURE PLANNING PHASE
**Date**: December 30, 2025

---

## 1. Executive Summary

This document provides the complete architectural plan for Phase II implementation, transforming the single-user CLI application into a professional, scalable multi-user web application. It defines:

- **Monorepo Structure**: How frontend, backend, and shared packages are organized
- **Component Responsibilities**: Clear boundaries and functions of each layer
- **Integration Points**: How frontend and backend communicate
- **JWT Authentication Flow**: Complete token lifecycle and validation
- **Data Flow Architecture**: How data moves through the system
- **Scalability Considerations**: Design decisions enabling future growth

### Architecture Principles
1. **Separation of Concerns**: Clear boundaries between frontend, backend, database
2. **Stateless API**: Backend doesn't maintain user sessions
3. **JWT-based Auth**: Tokens replace server-side session storage
4. **RESTful Design**: Standard HTTP methods for resource operations
5. **Type Safety**: TypeScript on frontend, type hints in Python backend
6. **API-First Development**: Frontend and backend developed in parallel

---

## 2. Monorepo Structure and Organization

### 2.1 Repository Layout

```
python-cli-todo/ (root)
├── .github/
│   └── workflows/              # CI/CD pipelines
│       ├── backend-tests.yml
│       ├── frontend-tests.yml
│       ├── deploy-backend.yml
│       └── deploy-frontend.yml
│
├── packages/                   # Shared code
│   ├── shared-types/
│   │   ├── package.json
│   │   └── src/
│   │       ├── types/
│   │       │   ├── auth.ts
│   │       │   ├── task.ts
│   │       │   ├── user.ts
│   │       │   └── api.ts
│   │       ├── constants/
│   │       │   ├── status.ts
│   │       │   ├── priority.ts
│   │       │   └── errors.ts
│   │       └── utils/
│   │           ├── validation.ts
│   │           └── formatting.ts
│   │
│   └── shared-schema/          # Pydantic/TypeScript shared schema
│       ├── pyproject.toml
│       └── src/
│           ├── models/
│           │   ├── task.py
│           │   └── user.py
│           └── validators/
│
├── apps/
│   │
│   ├── frontend/               # Next.js application
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   ├── next.config.js
│   │   ├── .env.example
│   │   ├── public/             # Static assets
│   │   ├── src/
│   │   │   ├── app/            # App Router pages
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── page.tsx
│   │   │   │   ├── (auth)/
│   │   │   │   │   ├── login/page.tsx
│   │   │   │   │   └── signup/page.tsx
│   │   │   │   ├── (dashboard)/
│   │   │   │   │   ├── layout.tsx
│   │   │   │   │   ├── page.tsx
│   │   │   │   │   ├── tasks/
│   │   │   │   │   └── settings/
│   │   │   │   └── api/
│   │   │   │       └── [...proxy].ts
│   │   │   ├── components/
│   │   │   │   ├── Layout/
│   │   │   │   │   ├── Navigation.tsx
│   │   │   │   │   ├── Sidebar.tsx
│   │   │   │   │   └── Footer.tsx
│   │   │   │   ├── Auth/
│   │   │   │   │   ├── LoginForm.tsx
│   │   │   │   │   └── SignUpForm.tsx
│   │   │   │   ├── Tasks/
│   │   │   │   │   ├── TaskCard.tsx
│   │   │   │   │   ├── TaskForm.tsx
│   │   │   │   │   ├── TaskList.tsx
│   │   │   │   │   └── TaskFilter.tsx
│   │   │   │   └── Common/
│   │   │   │       ├── Loading.tsx
│   │   │   │       ├── Error.tsx
│   │   │   │       ├── Modal.tsx
│   │   │   │       └── Toast.tsx
│   │   │   ├── hooks/
│   │   │   │   ├── useAuth.ts
│   │   │   │   ├── useTask.ts
│   │   │   │   ├── useFetch.ts
│   │   │   │   └── useLocalStorage.ts
│   │   │   ├── services/
│   │   │   │   ├── api.ts        # Base API client
│   │   │   │   ├── auth.ts       # Auth endpoints
│   │   │   │   └── tasks.ts      # Task endpoints
│   │   │   ├── context/
│   │   │   │   ├── AuthContext.tsx
│   │   │   │   ├── TaskContext.tsx
│   │   │   │   └── UIContext.tsx
│   │   │   ├── utils/
│   │   │   │   ├── axios.ts      # HTTP client config
│   │   │   │   ├── jwt.ts        # JWT utilities
│   │   │   │   ├── storage.ts    # Token storage
│   │   │   │   └── format.ts     # Display formatting
│   │   │   ├── types/
│   │   │   │   └── index.ts      # Shared types
│   │   │   └── styles/
│   │   │       └── globals.css
│   │   └── tests/
│   │       ├── __tests__/
│   │       │   ├── components/
│   │       │   ├── hooks/
│   │       │   ├── services/
│   │   │       └── integration/
│   │       └── jest.config.js
│   │
│   └── backend/                # FastAPI application
│       ├── pyproject.toml
│       ├── requirements.txt
│       ├── requirements-dev.txt
│       ├── .env.example
│       ├── alembic/            # Database migrations
│       │   ├── env.py
│       │   ├── script.py.mako
│       │   ├── versions/
│       │   └── alembic.ini
│       ├── src/
│       │   └── app/
│       │       ├── __main__.py  # Entry point
│       │       ├── main.py      # FastAPI app initialization
│       │       ├── config.py    # Configuration
│       │       ├── database.py  # Database setup
│       │       ├── security.py  # JWT and auth logic
│       │       ├── models/
│       │       │   ├── user.py
│       │       │   ├── task.py
│       │       │   └── base.py
│       │       ├── schemas/
│       │       │   ├── user.py
│       │       │   ├── task.py
│       │       │   └── auth.py
│       │       ├── crud/
│       │       │   ├── user.py
│       │       │   └── task.py
│       │       ├── api/
│       │       │   └── v1/
│       │       │       ├── __init__.py
│       │       │       ├── router.py
│       │       │       ├── endpoints/
│       │       │       │   ├── auth.py
│       │       │       │   ├── tasks.py
│       │       │       │   ├── users.py
│       │       │       │   └── health.py
│       │       │       └── dependencies.py
│       │       ├── services/
│       │       │   ├── auth.py
│       │       │   ├── user.py
│       │       │   └── task.py
│       │       ├── utils/
│       │       │   ├── validators.py
│       │       │   ├── formatters.py
│       │       │   └── exceptions.py
│       │       └── middleware/
│       │           ├── cors.py
│       │           ├── error_handler.py
│       │           └── logging.py
│       ├── tests/
│       │   ├── __init__.py
│       │   ├── conftest.py
│       │   ├── test_auth.py
│       │   ├── test_tasks.py
│       │   └── integration/
│       │       └── test_workflows.py
│       └── docker/
│           └── Dockerfile
│
├── docs/
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   └── DATABASE.md
│
├── specs/
│   ├── phase1/
│   │   ├── constitution.md
│   │   ├── specify.md
│   │   ├── plan.md
│   │   └── tasks.md
│   └── phase2/
│       ├── constitution.md (optional)
│       ├── specify.md
│       ├── plan.md (this file)
│       └── tasks.md (to be created)
│
├── docker-compose.yml         # Local development database
├── .env.example              # Environment template
├── .gitignore                # Git ignore patterns
├── README.md                 # Project overview
└── DEVELOPMENT.md            # Development guide
```

### 2.2 Package Responsibilities

#### **shared-types** (TypeScript)
**Purpose**: Centralized type definitions used across frontend

**Responsibilities**:
- Define TypeScript interfaces for API responses
- Define validation constants (field lengths, status values)
- Export shared error codes and messages
- Provide reusable utility types

**Consumers**:
- Frontend application
- Frontend tests
- Backend documentation (reference)

**Example Contents**:
```
- TaskType: Interface for task object
- UserType: Interface for user object
- AuthResponse: Interface for auth endpoint responses
- ApiError: Standard error response shape
- StatusEnum: 'pending' | 'completed'
- PriorityEnum: 'low' | 'medium' | 'high'
```

**Why Separate Package**:
- Reduces duplication
- Enables type checking across projects
- Shared constants in single source of truth
- Can be versioned independently

#### **shared-schema** (Python)
**Purpose**: Shared Pydantic models used by backend

**Responsibilities**:
- Define Pydantic BaseModel classes
- Validation logic at schema level
- Serialization/deserialization helpers
- Shared error handling patterns

**Consumers**:
- FastAPI backend
- Backend tests
- Documentation generation

**Example Contents**:
```
- TaskCreate: Schema for task creation
- TaskResponse: Schema for task response
- UserCreate: Schema for user creation
- UserResponse: Schema for user response
```

**Why Separate Package**:
- Centralized validation
- Reusable schemas across endpoints
- Easy to extend with custom validators
- Can be imported in different modules

#### **frontend** (Next.js)
**Purpose**: User-facing web application

**Responsibilities**:
- Render pages and components
- Handle user interactions
- Call backend APIs
- Manage local state
- Display data to users
- Handle errors and loading states

**Key Directories**:
- `app/`: Next.js App Router pages
- `components/`: React components
- `hooks/`: Custom React hooks
- `services/`: API client functions
- `context/`: Context providers
- `utils/`: Helper functions
- `types/`: TypeScript interfaces

**Testing**:
- Unit tests: Components, hooks, utilities
- Integration tests: User workflows
- E2E tests: Full page interactions

#### **backend** (FastAPI)
**Purpose**: REST API server

**Responsibilities**:
- Accept HTTP requests
- Validate input data
- Authenticate and authorize users
- Perform business logic
- Query and update database
- Return JSON responses
- Handle errors

**Key Directories**:
- `models/`: SQLModel database models
- `schemas/`: Pydantic request/response schemas
- `crud/`: Database operations
- `services/`: Business logic
- `api/endpoints/`: Route handlers
- `middleware/`: Request/response processing
- `utils/`: Helper functions

**Testing**:
- Unit tests: Business logic, schemas
- Integration tests: API endpoints
- Database tests: CRUD operations

---

## 3. Layered Architecture

### 3.1 Frontend Architecture Layers

```
┌─────────────────────────────────────┐
│   Presentation Layer                │
│   (Pages, Components, UI)           │
├─────────────────────────────────────┤
│   State Management Layer             │
│   (Context, Hooks, Providers)       │
├─────────────────────────────────────┤
│   Service Layer                      │
│   (API Clients, Data Fetching)      │
├─────────────────────────────────────┤
│   Utility Layer                      │
│   (Helpers, Formatters, Validators) │
├─────────────────────────────────────┤
│   Network Layer                      │
│   (HTTP Client, Interceptors)       │
└─────────────────────────────────────┘
```

**Presentation Layer**:
- Pages: Full page components from App Router
- Components: Reusable UI components
- Layouts: Shared layout structure
- Responsibility: Render UI, collect user input

**State Management Layer**:
- Context providers: AuthContext, TaskContext
- Custom hooks: useAuth, useTask, useFetch
- Local component state
- Responsibility: Maintain app state, provide to components

**Service Layer**:
- API client functions
- Data transformation
- Cache management
- Responsibility: Interact with backend

**Utility Layer**:
- Format dates, currencies
- Validate form inputs
- Parse JWT tokens
- Responsibility: Support other layers

**Network Layer**:
- HTTP client configuration
- Interceptors for tokens
- Error handling
- Responsibility: Send requests, handle responses

### 3.2 Backend Architecture Layers

```
┌─────────────────────────────────────┐
│   API Layer                         │
│   (Routes, Endpoints)               │
├─────────────────────────────────────┤
│   Service Layer                      │
│   (Business Logic)                  │
├─────────────────────────────────────┤
│   Data Access Layer                 │
│   (CRUD Operations)                 │
├─────────────────────────────────────┤
│   Model Layer                        │
│   (Database Models)                 │
├─────────────────────────────────────┤
│   Database Layer                     │
│   (PostgreSQL)                      │
└─────────────────────────────────────┘
```

**API Layer** (`api/endpoints/`):
- Route definitions: @router.get(), @router.post()
- Request parsing: Extract from path, query, body
- Response formatting: Serialize models to schemas
- Responsibility: Handle HTTP requests/responses

**Service Layer** (`services/`):
- Business logic: Validate, calculate, transform
- Orchestration: Call multiple CRUD operations
- Authentication: Verify tokens, validate permissions
- Responsibility: Implement domain logic

**Data Access Layer** (`crud/`):
- CRUD operations: Create, read, update, delete
- Querying: Filter, sort, paginate
- Database session management
- Responsibility: Interact with database

**Model Layer** (`models/`):
- SQLModel classes: Define table structure
- Relationships: User → Tasks
- Validators: Field-level validation
- Responsibility: Define data schema

**Database Layer**:
- PostgreSQL connection
- Transaction management
- Connection pooling
- Responsibility: Persistent storage

---

## 4. Data Flow Architecture

### 4.1 Complete User Request Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        USER BROWSER                         │
│  (Frontend: Next.js React Components)                       │
└────────────────────┬────────────────────────────────────────┘
                     │ 1. User interaction (click, submit)
                     │
┌────────────────────▼────────────────────────────────────────┐
│           EVENT HANDLER / FORM HANDLER                      │
│  (Component onSubmit, onClick, onChange)                    │
└────────────────────┬────────────────────────────────────────┘
                     │ 2. Dispatch action or call service
                     │
┌────────────────────▼────────────────────────────────────────┐
│              SERVICE LAYER (API CLIENT)                     │
│  (services/tasks.ts, services/auth.ts)                      │
│                                                              │
│  ├─ 2a. Format request data                                │
│  ├─ 2b. Validate data                                      │
│  └─ 2c. Call HTTP client                                   │
└────────────────────┬────────────────────────────────────────┘
                     │ 3. HTTP request
                     │    Authorization: Bearer {token}
                     │    Content-Type: application/json
                     │
┌────────────────────▼────────────────────────────────────────┐
│              NETWORK LAYER (HTTP CLIENT)                    │
│  (utils/axios.ts or Fetch API)                             │
│                                                              │
│  ├─ Interceptor: Add JWT token header                       │
│  ├─ Send request to backend                                │
│  └─ Return response or error                               │
└────────────────────┬────────────────────────────────────────┘
                     │ 4. Network transmission (HTTPS)
                     │
        ┌────────────▼────────────┐
        │  INTERNET / NETWORK     │
        │  POST /api/tasks        │
        │  Authorization: Bearer  │
        │  {JWT token}            │
        └────────────▲────────────┘
                     │ 5. HTTPS request arrives
                     │
┌────────────────────┴────────────────────────────────────────┐
│                     BACKEND (FastAPI)                       │
└────────────────────┬────────────────────────────────────────┘
                     │ 6. Request routing
                     │
┌────────────────────▼────────────────────────────────────────┐
│         MIDDLEWARE & CORS HANDLING                          │
│  (middleware/cors.py)                                       │
│                                                              │
│  ├─ Check origin                                           │
│  ├─ Handle preflight (OPTIONS)                             │
│  └─ Pass to next middleware                                │
└────────────────────┬────────────────────────────────────────┘
                     │ 7. Route to endpoint
                     │
┌────────────────────▼────────────────────────────────────────┐
│              API LAYER (ENDPOINTS)                          │
│  (api/endpoints/tasks.py → @router.post("/"))              │
│                                                              │
│  ├─ 7a. Dependency injection                               │
│  ├─ 7b. Extract path/query params                          │
│  └─ 7c. Parse request body                                 │
└────────────────────┬────────────────────────────────────────┘
                     │ 8. Request body to Pydantic schema
                     │
┌────────────────────▼────────────────────────────────────────┐
│            DEPENDENCY INJECTION                             │
│  (api/dependencies.py → get_current_user())                │
│                                                              │
│  ├─ 8a. Extract JWT from Authorization header              │
│  ├─ 8b. Verify JWT signature and expiration                │
│  ├─ 8c. Extract user_id from token                         │
│  ├─ 8d. Query database for user                            │
│  └─ 8e. Return user object or raise 401 error             │
└────────────────────┬────────────────────────────────────────┘
                     │ 9. Call endpoint handler
                     │
┌────────────────────▼────────────────────────────────────────┐
│           SERVICE LAYER (BUSINESS LOGIC)                    │
│  (services/task.py → create_task())                         │
│                                                              │
│  ├─ 9a. Validate input (title length, etc.)                │
│  ├─ 9b. Check permissions (user can create tasks)          │
│  ├─ 9c. Perform business logic                             │
│  └─ 9d. Call CRUD layer                                    │
└────────────────────┬────────────────────────────────────────┘
                     │ 10. CRUD operation
                     │
┌────────────────────▼────────────────────────────────────────┐
│         DATA ACCESS LAYER (CRUD)                            │
│  (crud/task.py → create_task())                             │
│                                                              │
│  ├─ 10a. Create Task model instance                        │
│  ├─ 10b. Add to database session                           │
│  ├─ 10c. Commit transaction                                │
│  └─ 10d. Refresh to get ID                                 │
└────────────────────┬────────────────────────────────────────┘
                     │ 11. SQL query
                     │
┌────────────────────▼────────────────────────────────────────┐
│             DATABASE LAYER (PostgreSQL)                     │
│  (Neon PostgreSQL)                                          │
│                                                              │
│  ├─ INSERT INTO tasks (title, user_id, ...)                │
│  ├─ RETURNING id, created_at, ...                          │
│  └─ Row inserted and returned                              │
└────────────────────┬────────────────────────────────────────┘
                     │ 12. Task model with generated ID
                     │
┌────────────────────▼────────────────────────────────────────┐
│            RESPONSE FORMATTING                              │
│  (Endpoint handler → return TaskResponse)                   │
│                                                              │
│  ├─ Convert Task model to TaskResponse schema              │
│  ├─ Serialize to JSON                                      │
│  └─ Set status code 201 Created                            │
└────────────────────┬────────────────────────────────────────┘
                     │ 13. JSON response
                     │    {
                     │      "id": "uuid",
                     │      "title": "...",
                     │      "created_at": "..."
                     │    }
                     │
┌────────────────────▼────────────────────────────────────────┐
│            RESPONSE TRANSMISSION                            │
│  (HTTPS response)                                           │
│                                                              │
│  Status: 201 Created                                        │
│  Content-Type: application/json                             │
└────────────────────┬────────────────────────────────────────┘
                     │ 14. Network transmission (HTTPS)
                     │
        ┌────────────▼────────────┐
        │  INTERNET / NETWORK     │
        │  JSON response          │
        └────────────▲────────────┘
                     │ 15. Response arrives at frontend
                     │
┌────────────────────┴────────────────────────────────────────┐
│          NETWORK LAYER (HTTP CLIENT)                        │
│  (utils/axios.ts or Fetch API)                             │
│                                                              │
│  ├─ Parse response                                         │
│  ├─ Check status code                                      │
│  └─ Return data or throw error                             │
└────────────────────┬────────────────────────────────────────┘
                     │ 16. Return to service
                     │
┌────────────────────▼────────────────────────────────────────┐
│            SERVICE LAYER (API CLIENT)                       │
│  (services/tasks.ts)                                        │
│                                                              │
│  ├─ Receive response                                       │
│  ├─ Transform data if needed                               │
│  └─ Return to caller                                       │
└────────────────────┬────────────────────────────────────────┘
                     │ 17. Return to component
                     │
┌────────────────────▼────────────────────────────────────────┐
│         STATE MANAGEMENT (Context or Hook)                  │
│  (useTask hook or TaskContext)                             │
│                                                              │
│  ├─ Update state with new task                             │
│  ├─ Set loading to false                                   │
│  └─ Clear error message                                    │
└────────────────────┬────────────────────────────────────────┘
                     │ 18. Component re-renders
                     │
┌────────────────────▼────────────────────────────────────────┐
│         PRESENTATION LAYER (React Component)                │
│  (components/TaskCard.tsx, pages/tasks/page.tsx)           │
│                                                              │
│  ├─ Receive updated state as props                         │
│  ├─ Re-render with new task                                │
│  └─ Display "Task created!" toast                          │
└────────────────────┬────────────────────────────────────────┘
                     │ 19. User sees new task
                     │    in task list
                     │
┌────────────────────▼────────────────────────────────────────┐
│                        USER BROWSER                         │
│            (Updated UI with new task)                       │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Read Operation Flow (GET /api/tasks)

```
User clicks "View Tasks"
        │
        ▼
useTask hook called
        │
        ├─ Check AuthContext for token
        │
        ▼
services/tasks.ts → getTasks()
        │
        ├─ Make HTTP GET request
        ├─ Include Authorization header
        │
        ▼
Backend: GET /api/tasks endpoint
        │
        ├─ get_current_user() dependency
        │   └─ Verify JWT token
        │
        ├─ Call services/task.py → get_user_tasks()
        │   │
        │   ├─ Filter tasks by user_id
        │   ├─ Apply filters/sorting
        │   └─ Return list of Task models
        │
        ├─ Convert Task models to TaskResponse schema
        │
        ▼
Return JSON array of tasks
        │
        ▼
Frontend service receives response
        │
        ├─ Update TaskContext state
        │
        ▼
Component re-renders
        │
        ├─ Display task list
        │
        ▼
User sees tasks
```

### 4.3 Write Operation Flow (PATCH /api/tasks/{id})

```
User edits task and clicks Save
        │
        ▼
Form submission handler
        │
        ├─ Validate input locally
        │
        ▼
services/tasks.ts → updateTask(id, data)
        │
        ├─ Make HTTP PATCH request
        ├─ Include Authorization header
        ├─ Include updated fields in body
        │
        ▼
Backend: PATCH /api/tasks/{id} endpoint
        │
        ├─ get_current_user() dependency
        │   └─ Verify JWT token
        │
        ├─ Parse path parameter (task_id)
        │
        ├─ Validate request body with Pydantic
        │
        ├─ Call services/task.py → update_task()
        │   │
        │   ├─ Check: user owns task
        │   ├─ Validate: fields (title length, etc.)
        │   ├─ Call CRUD: crud/task.py → update()
        │   │   │
        │   │   ├─ Query database for task
        │   │   ├─ Update fields
        │   │   ├─ Commit transaction
        │   │   └─ Return updated Task model
        │   │
        │   └─ Return updated task
        │
        ├─ Convert Task model to TaskResponse schema
        │
        ▼
Return updated task as JSON
        │
        ▼
Frontend service receives response
        │
        ├─ Update TaskContext with new task
        │
        ▼
Component re-renders
        │
        ├─ Display updated task
        ├─ Show success toast
        │
        ▼
User sees updated task
```

---

## 5. JWT Authentication Flow

### 5.1 Token Generation and Structure

#### User Signs Up or Logs In
```
POST /api/auth/signup or /api/auth/login
├─ Receive: email, password
│
├─ Backend processing:
│  ├─ Hash password with bcrypt
│  ├─ Store in database
│  └─ Create JWT tokens
│
└─ Return:
   ├─ access_token (15 min expiration)
   ├─ refresh_token (7 day expiration)
   └─ user object
```

#### Access Token Structure
```
Header:
{
  "alg": "HS256",      // Algorithm
  "typ": "JWT"         // Type
}

Payload:
{
  "sub": "user-uuid",           // Subject (user ID)
  "email": "user@example.com",  // Email
  "username": "johndoe",        // Username
  "iat": 1703944800,            // Issued at
  "exp": 1703945700,            // Expires at (15 min later)
  "type": "access"              // Token type
}

Signature:
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  "jwt-secret-key"
)
```

#### Refresh Token Structure
```
Header:
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload:
{
  "sub": "user-uuid",           // Subject (user ID)
  "iat": 1703944800,            // Issued at
  "exp": 1704549600,            // Expires at (7 days later)
  "type": "refresh"             // Token type
}

Signature: (same algorithm)
```

### 5.2 Frontend Token Storage

```
POST /api/auth/login
├─ Send credentials
│
▼
Receive: { access_token, refresh_token, user }
│
├─ Store in Context:
│  ├─ localStorage.setItem('accessToken', access_token)
│  ├─ localStorage.setItem('refreshToken', refresh_token)
│  └─ AuthContext.user = user
│
└─ Redirect to dashboard
```

**Storage Options**:

Option 1: **localStorage** (Current Plan)
- Pros: Simple, persists across browser close, works in SSR
- Cons: Vulnerable to XSS attacks
- Usage: Frontend stores tokens, includes in every API request

Option 2: **httpOnly Cookies** (More Secure)
- Pros: Secure from XSS, automatic inclusion in requests
- Cons: Requires backend to set cookie, CSRF risk
- Usage: Backend sets cookie, browser sends automatically

Option 3: **Memory Only** (Most Secure)
- Pros: No persistent storage vulnerability
- Cons: Lost on page refresh
- Usage: Combined with auto-refresh via refresh token

**Phase II Choice**: localStorage (simpler), upgrade to httpOnly in Phase II+

### 5.3 Token Inclusion in API Requests

#### Axios Interceptor
```
Every HTTP request:

GET /api/tasks
├─ Interceptor runs before sending
│
├─ Retrieve token from localStorage
│  └─ accessToken = localStorage.getItem('accessToken')
│
├─ Add to headers
│  └─ Authorization: Bearer {accessToken}
│
└─ Send request with header
```

#### Manual Fetch API
```
fetch('/api/tasks', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
```

### 5.4 Server-Side Token Verification

```
Backend receives: GET /api/tasks
│
├─ Extract Authorization header
│  └─ "Bearer eyJhbGc..."
│
├─ Parse token
│  ├─ Split by space: ["Bearer", "eyJhbGc..."]
│  └─ Get token part
│
├─ Verify JWT signature
│  ├─ Decode header
│  ├─ Decode payload
│  ├─ Verify signature matches
│  └─ If invalid: raise HTTPException(status_code=401)
│
├─ Check expiration
│  ├─ Extract 'exp' from payload
│  ├─ Compare with current time
│  └─ If expired: raise HTTPException(status_code=401)
│
├─ Extract user_id from 'sub'
│  └─ user_id = payload['sub']
│
├─ Query database for user
│  ├─ user = db.query(User).filter(User.id == user_id).first()
│  └─ If not found: raise HTTPException(status_code=401)
│
└─ Return user object to endpoint
   └─ Endpoint receives authenticated user
```

**Dependency Injection in FastAPI**:
```
@router.get("/tasks")
async def list_tasks(
    current_user: User = Depends(get_current_user)
):
    # current_user is now available
    # Only trusted code reaches here
```

### 5.5 Token Refresh Flow

#### Access Token Expires
```
Frontend: API call with expired token
│
├─ Request fails with 401 Unauthorized
│
├─ Frontend catches error
│  └─ Check if token expired
│
├─ If expired, call refresh endpoint
│  └─ POST /api/auth/refresh
│     ├─ Include refresh_token
│     └─ Request new tokens
│
├─ Backend processes refresh request
│  ├─ Verify refresh_token signature
│  ├─ Check expiration
│  ├─ Check token type is 'refresh'
│  ├─ If valid: generate new tokens
│  └─ If invalid: raise 401 error
│
├─ Frontend receives new tokens
│  ├─ localStorage.setItem('accessToken', newAccessToken)
│  ├─ localStorage.setItem('refreshToken', newRefreshToken)
│  └─ AuthContext.tokens = { access, refresh }
│
└─ Retry original request with new token
```

**Automatic Retry with Interceptor**:
```
Request fails with 401
    │
    ▼
Response interceptor catches error
    │
    ├─ Check if 401 and refresh_token exists
    │
    ├─ Call POST /api/auth/refresh
    │
    ├─ Get new access_token
    │
    ├─ Update localStorage and context
    │
    └─ Retry original request with new token
```

### 5.6 Logout Flow

```
User clicks "Logout"
│
├─ Event handler triggered
│
├─ Clear frontend storage
│  ├─ localStorage.removeItem('accessToken')
│  ├─ localStorage.removeItem('refreshToken')
│  └─ AuthContext.user = null
│
├─ Call logout endpoint (optional)
│  └─ POST /api/auth/logout
│     ├─ Validate token
│     └─ Server-side cleanup (optional)
│
├─ Clear cookies (if using httpOnly)
│  └─ Backend sends Set-Cookie with Max-Age=0
│
└─ Redirect to login page
```

### 5.7 Token Expiration Scenarios

#### Scenario 1: Access Token Expires During Session
```
User is actively using app
    │
    ├─ Access token expires (15 min)
    │
    ├─ Next API call fails with 401
    │
    ├─ Refresh token is still valid (7 days)
    │
    ├─ Frontend automatically calls refresh endpoint
    │
    ├─ Backend returns new access token
    │
    └─ User continues without logging in
```

#### Scenario 2: Refresh Token Expires
```
User inactive for 7 days
    │
    ├─ Refresh token expires
    │
    ├─ User tries to use app
    │
    ├─ Access token also expired
    │
    ├─ Try to refresh → fails (refresh token expired)
    │
    ├─ Redirect to login page
    │
    └─ User must log in again
```

#### Scenario 3: Suspicious Token Activity
```
Token appears invalid or tampered
    │
    ├─ Signature verification fails
    │
    ├─ Return 401 Unauthorized
    │
    └─ Redirect to login page
```

---

## 6. Frontend-Backend Integration Points

### 6.1 API Client Architecture

#### Base API Client (utils/axios.ts)
```
Purpose: Centralized HTTP client configuration

Responsibilities:
├─ Create axios/fetch instance
├─ Configure base URL
├─ Add auth token to headers
├─ Handle response transformation
├─ Handle error responses
├─ Implement request/response interceptors
└─ Implement refresh token logic

Usage:
├─ Import in service files
├─ Use for all API calls
└─ Ensures consistent behavior across app
```

#### Service Layer (services/)
```
Purpose: Encapsulate API calls and data transformation

Structure:
├─ services/auth.ts
│  ├─ signup(email, password, name)
│  ├─ login(email, password)
│  ├─ refresh()
│  ├─ logout()
│  └─ getCurrentUser()
│
├─ services/tasks.ts
│  ├─ getTasks(filters)
│  ├─ getTask(id)
│  ├─ createTask(title, description, ...)
│  ├─ updateTask(id, updates)
│  ├─ updateTaskStatus(id, status)
│  └─ deleteTask(id)
│
└─ services/users.ts
   ├─ getProfile()
   └─ updateProfile(updates)

Pattern:
const getTasks = async (filters) => {
  try {
    const response = await apiClient.get('/api/tasks', {
      params: filters
    });
    return response.data;
  } catch (error) {
    throw new ApiError(error);
  }
};
```

### 6.2 Authentication Integration

#### Frontend: Auth Context
```
AuthContext provides:
├─ user: Current user object (or null)
├─ isLoading: Whether auth is being checked
├─ isAuthenticated: Boolean flag
├─ tokens: { accessToken, refreshToken }
│
└─ Methods:
   ├─ signup(email, password, name)
   │  ├─ Call services/auth.signup()
   │  ├─ Store tokens
   │  ├─ Store user
   │  └─ Redirect to dashboard
   │
   ├─ login(email, password)
   │  ├─ Call services/auth.login()
   │  ├─ Store tokens
   │  ├─ Store user
   │  └─ Redirect to dashboard
   │
   └─ logout()
      ├─ Clear tokens
      ├─ Clear user
      └─ Redirect to login
```

#### Protected Routes
```
Layout-level protection:
├─ Check if user is authenticated
├─ If not: redirect to /login
├─ If yes: render dashboard
└─ Apply middleware or wrapper

Component-level protection:
├─ useAuth hook to get auth state
├─ useRouter to redirect if needed
└─ Guard sensitive operations
```

### 6.3 Data Synchronization

#### Optimistic Updates
```
When user submits form:

1. Optimistically update local state
   └─ Show new task in list immediately

2. Send request to backend
   └─ Async operation in background

3. If backend confirms
   └─ Keep local state (already updated)

4. If backend rejects
   ├─ Rollback local state
   └─ Show error message
```

#### Pessimistic Updates
```
When user submits form:

1. Show loading state
   └─ Disable submit button

2. Send request to backend
   └─ Wait for response

3. If backend confirms
   ├─ Update local state
   └─ Show success message

4. If backend rejects
   └─ Show error message
```

#### Polling vs Real-time
```
Polling (Phase II):
├─ Frontend periodically calls API
├─ GET /api/tasks every 5-10 seconds
└─ Checks for updates

Real-time (Future):
├─ WebSocket connection
├─ Server pushes updates
└─ No polling needed
```

### 6.4 Error Handling Integration

#### Frontend Error Handling
```
API call fails:
├─ Check status code
│
├─ 401 Unauthorized
│  └─ Redirect to login
│
├─ 403 Forbidden
│  └─ Show "Access denied" message
│
├─ 404 Not Found
│  └─ Show "Resource not found"
│
├─ 400 Bad Request
│  ├─ Validation error
│  └─ Show field-specific errors
│
├─ 500 Server Error
│  └─ Show "Server error, try again"
│
└─ Network error
   └─ Show "Connection failed" message
```

#### Backend Error Responses
```
Consistent error format:

{
  "detail": "User not found",
  "error_code": "USER_NOT_FOUND",
  "status": 404,
  "timestamp": "2025-12-30T10:00:00Z"
}

Validation errors:

{
  "detail": "Validation error",
  "errors": [
    {
      "field": "title",
      "message": "Title must be 1-255 characters"
    }
  ],
  "status": 422
}
```

### 6.5 Type Safety Integration

#### TypeScript Types from Backend
```
Shared types (from packages/shared-types/):

export interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string;
  status: 'pending' | 'completed';
  priority: 'low' | 'medium' | 'high';
  due_date: string | null;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

export interface User {
  id: string;
  email: string;
  username: string;
  full_name: string;
  avatar_url: string | null;
  created_at: string;
  updated_at: string;
}

Usage in frontend:
import { Task, User } from '@shared-types';

const handleCreateTask = async (data: TaskCreate): Promise<Task> => {
  return await apiClient.post('/api/tasks', data);
};
```

#### Python Type Hints
```
Backend uses Pydantic models:

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = 'medium'
    due_date: Optional[date] = None

class TaskResponse(TaskCreate):
    id: str
    user_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

@router.post("/tasks", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user)
) -> TaskResponse:
    ...
```

---

## 7. Deployment Architecture

### 7.1 Environment Separation

```
Development:
├─ Frontend: http://localhost:3000
├─ Backend: http://localhost:8000
├─ Database: localhost PostgreSQL
└─ JWT Secret: dev-secret-key

Staging:
├─ Frontend: staging-app.example.com
├─ Backend: api-staging.example.com
├─ Database: Neon staging branch
└─ JWT Secret: staging-secret-key

Production:
├─ Frontend: app.example.com (Vercel)
├─ Backend: api.example.com (Cloud host)
├─ Database: Neon production
└─ JWT Secret: prod-secret-key (secrets manager)
```

### 7.2 CORS Configuration

```
Frontend needs to access backend:

Backend CORS middleware:
├─ Allow origins: http://localhost:3000, app.example.com
├─ Allow methods: GET, POST, PATCH, DELETE, OPTIONS
├─ Allow headers: Content-Type, Authorization
├─ Allow credentials: true (for cookies)
└─ Max age: 3600 seconds

Example configuration:
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://app.example.com",
        "https://staging-app.example.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 7.3 Deployment Pipeline

```
Developer commits code
        │
        ▼
GitHub Actions CI/CD
        │
        ├─ Run frontend tests
        ├─ Run backend tests
        ├─ Check TypeScript/Python types
        └─ Build artifacts
        │
        ├─ If tests pass:
        │  ├─ Deploy frontend to Vercel
        │  ├─ Deploy backend to host
        │  └─ Run database migrations
        │
        └─ If tests fail:
           └─ Reject deployment
```

---

## 8. Database Architecture

### 8.1 Schema Design

```
users (table)
├─ id: UUID (PK)
├─ email: VARCHAR (UNIQUE)
├─ username: VARCHAR (UNIQUE)
├─ password_hash: VARCHAR
├─ full_name: VARCHAR
├─ avatar_url: VARCHAR (NULL)
├─ is_active: BOOLEAN
├─ created_at: TIMESTAMP
└─ updated_at: TIMESTAMP

tasks (table)
├─ id: UUID (PK)
├─ user_id: UUID (FK → users.id)
├─ title: VARCHAR
├─ description: TEXT
├─ status: VARCHAR (pending/completed)
├─ priority: VARCHAR (low/medium/high)
├─ due_date: DATE (NULL)
├─ created_at: TIMESTAMP
├─ updated_at: TIMESTAMP
└─ completed_at: TIMESTAMP (NULL)

Indexes:
├─ PRIMARY KEY: id
├─ FOREIGN KEY: user_id
├─ UNIQUE: email, username
└─ COMPOSITE: (user_id, status)
```

### 8.2 Migrations

```
Alembic manages schema changes:

alembic/versions/
├─ 001_initial_schema.py
│  └─ Create users and tasks tables
│
├─ 002_add_priority_to_tasks.py
│  └─ Add priority column (Phase II enhancement)
│
└─ 003_add_due_date_to_tasks.py
   └─ Add due_date column (Phase II enhancement)

Deployment:
├─ Run migrations: alembic upgrade head
└─ Rollback if needed: alembic downgrade -1
```

---

## 9. Component Communication Patterns

### 9.1 Parent-Child Communication

```
Component Hierarchy:
DashboardLayout
├─ TaskList
│  ├─ TaskCard (multiple)
│  └─ TaskFilter
├─ TaskForm
│  └─ (modal)
└─ Navigation

Data Flow:
DashboardLayout (state)
    │
    ├─ Pass tasks to TaskList (prop)
    │   └─ TaskList maps to TaskCard components
    │
    ├─ Pass onCreateTask callback to TaskForm
    │   └─ TaskForm calls callback on submit
    │
    └─ TaskCard sends delete request up the chain
        └─ DashboardLayout handles deletion
```

### 9.2 Context for Global State

```
AuthContext
├─ Provides: user, tokens, isAuthenticated
├─ Consumed by: All protected pages, Navigation
└─ Updates via: login(), logout(), refresh()

TaskContext
├─ Provides: tasks, selectedTask, filters
├─ Consumed by: TaskList, TaskDetail, TaskForm
└─ Updates via: create, update, delete methods

UIContext
├─ Provides: theme, sidebarOpen, notifications
├─ Consumed by: Layout, Navigation, Toast
└─ Updates via: toggle theme, show toast, etc.
```

### 9.3 Props Drilling vs Context

```
Avoid props drilling:
❌ DashboardLayout → TaskList → TaskCard → TaskActions
   (4 levels deep)

Use Context instead:
✓ AuthContext provides user
✓ TaskContext provides tasks and methods
✓ UIContext provides notifications

Rule of thumb:
├─ Global app state (auth, UI) → Context
├─ Local component state → useState
├─ Shared within tree → Props
└─ 3+ levels deep → Consider Context
```

---

## 10. Testing Strategy Architecture

### 10.1 Frontend Testing Pyramid

```
    /\
   /  \  E2E Tests (10%)
  /────\─────── Cypress, Playwright
 /      \       Full user workflows
/────────\────
|        |  Integration Tests (30%)
|  Inte- |  Jest + React Testing Library
|  gration─ Component interactions, API calls
|        |
────────────
| Unit Tests (60%)
| Jest
| Components, hooks, utilities
──────────────────────────────
```

**Unit Tests** (60% - 40-50 tests):
- Component rendering
- Hook behavior
- Service functions
- Utility functions

**Integration Tests** (30% - 20 tests):
- Component with child components
- Form submission flows
- Context interaction
- API call integration

**E2E Tests** (10% - 5-10 tests):
- Complete user workflows
- Sign up → create task → view
- Error handling paths
- Authentication flows

### 10.2 Backend Testing Pyramid

```
    /\
   /  \  E2E Tests (10%)
  /────\─────── Full API workflow tests
 /      \       Multiple endpoints
/────────\────
|        |  Integration Tests (30%)
|  Inte- |  Tests with real database
|  gration─ Multiple CRUD operations
|        |
────────────
| Unit Tests (60%)
| Service logic, CRUD operations
| No database, mocked dependencies
──────────────────────────────
```

**Unit Tests** (60% - 40-50 tests):
- Service logic
- Validators
- Schemas
- Utilities

**Integration Tests** (30% - 15-20 tests):
- CRUD operations with database
- API endpoint responses
- Authentication flows

**E2E Tests** (10% - 5 tests):
- Complete workflows
- Multi-step operations
- Error recovery

### 10.3 Test Database

```
Testing Database Approach:

Option 1: Test Database (PostgreSQL in Docker)
├─ docker-compose.yml spins up test DB
├─ Tests run against real database
├─ Teardown after each test
└─ Most accurate, slower

Option 2: SQLite (in-memory)
├─ Use SQLite for tests instead of PostgreSQL
├─ Faster, no external dependencies
├─ Less accurate (different SQL dialect)
└─ Good for unit tests

Option 3: Mock Database
├─ Mock SQLAlchemy session
├─ No real database
├─ Fast, but less accurate
└─ Good for unit tests

Phase II Choice: Option 1 (test PostgreSQL)
```

---

## 11. Scalability and Performance

### 11.1 Frontend Performance

```
Code Splitting:
├─ Split by route: lazy load pages
├─ Split by component: lazy load heavy components
├─ Compression: Enable gzip on Next.js
└─ Caching: HTTP cache headers

Image Optimization:
├─ Use Next.js Image component
├─ Serve WebP format
├─ Lazy load images
└─ Generate multiple sizes

Monitoring:
├─ Core Web Vitals
│  ├─ LCP (Largest Contentful Paint)
│  ├─ FID (First Input Delay)
│  └─ CLS (Cumulative Layout Shift)
├─ Bundle analysis
└─ Performance budgets
```

### 11.2 Backend Performance

```
Database Optimization:
├─ Indexes on user_id, status
├─ Pagination for list endpoints
├─ Eager loading relationships
└─ Query optimization with EXPLAIN

API Optimization:
├─ Limit response fields
├─ Compress responses (gzip)
├─ Cache common queries
└─ Rate limiting

Monitoring:
├─ Response times
├─ Database query times
├─ Error rates
└─ Resource usage
```

### 11.3 Database Optimization

```
Indexes:
├─ PRIMARY KEY: id (automatic)
├─ FOREIGN KEY: user_id on tasks
├─ UNIQUE: email, username
├─ COMPOSITE: (user_id, status) for filtering
└─ Additional: due_date for sorting

Connection Pooling:
├─ SQLAlchemy engine with pool
├─ pool_size: 10-20 connections
├─ max_overflow: 10 extra connections
└─ Prevents resource exhaustion
```

---

## 12. Security Architecture

### 12.1 Frontend Security

```
XSS Prevention:
├─ Never use dangerouslySetInnerHTML
├─ Sanitize user input
├─ Use libraries like DOMPurify
└─ Content Security Policy headers

CSRF Prevention:
├─ SameSite cookie attribute
├─ CSRF tokens (if using traditional cookies)
└─ POST/PATCH/DELETE require tokens

Token Security:
├─ Don't log tokens
├─ Don't embed in URLs
├─ Clear on logout
└─ Set expiration

Dependency Security:
├─ npm audit regularly
├─ Automated dependency updates
└─ Vulnerability scanning
```

### 12.2 Backend Security

```
Authentication:
├─ Password hashing: bcrypt 12+ rounds
├─ JWT verification: Validate signature
├─ Token expiration: 15 min access, 7 day refresh
└─ Logout: Optional token blacklist

Authorization:
├─ Check user ownership of resources
├─ Verify permissions before operations
└─ Row-level security

Input Validation:
├─ Pydantic validation on all endpoints
├─ Type checking
├─ Length constraints
└─ Format validation

HTTPS Only:
├─ Redirect HTTP to HTTPS
├─ HSTS header
└─ TLS 1.2+
```

### 12.3 Database Security

```
Access Control:
├─ Strong database credentials
├─ Separate read/write users (optional)
└─ Network access limits

Encryption:
├─ In-transit: SSL/TLS connections
├─ At-rest: Database encryption (Neon feature)
└─ Passwords: Bcrypt hashing

Backups:
├─ Regular automated backups
├─ Encrypted backup storage
└─ Test restore procedures
```

---

## 13. Configuration Management

### 13.1 Environment Variables

**Backend (.env format)**:
```
# Database
DATABASE_URL=postgresql://user:pass@host/db

# JWT
JWT_SECRET=min-32-character-random-string
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=["http://localhost:3000", "https://app.example.com"]

# Application
DEBUG=False
LOG_LEVEL=INFO
ENVIRONMENT=production
```

**Frontend (.env.local format)**:
```
# API Configuration
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_API_TIMEOUT=30000

# App Configuration
NEXT_PUBLIC_APP_NAME=Todo App
NEXT_PUBLIC_APP_VERSION=2.0.0

# Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=true
```

### 13.2 Secrets Management

```
Development:
├─ .env.local (gitignored)
└─ Stored locally

Staging/Production:
├─ Environment variables in deployment platform
├─ Secrets manager (AWS Secrets Manager, Vercel Secrets, etc.)
└─ Never commit secrets to git
```

---

## 14. Monitoring and Logging

### 14.1 Application Logging

```
Frontend:
├─ Console logs (development only)
├─ Error tracking (Sentry)
└─ Analytics (Vercel Analytics, Google Analytics)

Backend:
├─ Structured logging (JSON format)
├─ Log levels: DEBUG, INFO, WARNING, ERROR
├─ Request logging (method, path, status, duration)
├─ Error logging with stack traces
└─ Centralized log aggregation (optional)
```

### 14.2 Metrics and Monitoring

```
Frontend:
├─ Core Web Vitals
├─ Error rate
├─ API response times
└─ User engagement

Backend:
├─ Request latency
├─ Database query time
├─ Error rate
├─ Resource usage (CPU, memory)
└─ Database connection pool status

Database:
├─ Query performance
├─ Connection count
├─ Disk usage
└─ Backup status
```

---

## 15. Integration Workflow

### 15.1 Parallel Development

```
Frontend Team:
├─ Defines API contract in shared-types
├─ Implements pages and components
├─ Creates mock API responses
├─ Writes tests

Backend Team:
├─ Reads API contract from shared-types
├─ Implements endpoints
├─ Creates test database
├─ Writes tests

Both Teams:
├─ Document changes
├─ Review pull requests
├─ Run integration tests
└─ Deploy together
```

### 15.2 API Contract Definition

```
Process:
1. Define types in shared-types
   ├─ Request body shape
   ├─ Response body shape
   ├─ Error response shape
   └─ Status codes

2. Create mock endpoint responses
   ├─ Frontend uses mock data for development
   └─ No backend needed initially

3. Implement backend endpoints
   ├─ Match contract exactly
   └─ Integration tests verify contract

4. Integrate
   ├─ Update frontend to real endpoint
   ├─ Remove mock data
   └─ Run E2E tests

5. Deploy
   ├─ Deploy frontend and backend together
   └─ Or deploy separately if compatible
```

---

## 16. Architectural Decisions

### 16.1 Why This Architecture?

| Decision | Rationale |
|----------|-----------|
| Monorepo | Shared types, unified development, easier CI/CD |
| Next.js | Built-in routing, SSR, Vercel integration, TypeScript |
| FastAPI | Python strength, async support, automatic docs, type hints |
| SQLModel | Combines SQLAlchemy + Pydantic, single model definition |
| JWT Tokens | Stateless, scalable, no server-side session storage |
| PostgreSQL | ACID compliance, relational, powerful queries, reliable |
| REST API | Simple, standard, widely understood, no complexity |
| Separate Repos | Clear responsibilities, independent scaling, easier management |

### 16.2 Trade-offs and Alternatives

```
Decision: Monorepo vs Separate Repositories

Monorepo (Chosen):
+ Shared types easier to maintain
+ Atomic commits across frontend/backend
+ Unified CI/CD pipeline
- Larger repository
- Potential merge conflicts
- Both teams need to understand structure

Separate Repos:
+ Smaller individual repos
+ Clear separation
- Type duplication
- Harder to keep in sync
- Multiple deployments

Decision: JWT vs Sessions

JWT (Chosen):
+ Stateless, no session storage needed
+ Easily scalable
+ Works across multiple servers
- Cannot revoke tokens immediately
- Refresh token complexity

Sessions:
+ Can revoke immediately
+ Simpler token management
- Require server-side storage
- Harder to scale
- Need sticky sessions

Decision: REST vs GraphQL

REST (Chosen):
+ Simple, standard
+ Easy to understand
+ Built-in HTTP caching
+ Standard tools and libraries

GraphQL:
+ Flexible querying
+ Reduced over-fetching
- Learning curve
- More complex
- Caching harder
- Not ideal for simple CRUD
```

---

## 17. Future Scalability

### 17.1 Horizontal Scaling

```
Current:
┌─────────────┐
│  Frontend   │
└──────┬──────┘
       │
┌──────▼──────┐
│  Backend    │
└──────┬──────┘
       │
┌──────▼──────┐
│  Database   │
└─────────────┘

Future with Load Balancing:
┌──────────────────────────────┐
│      Load Balancer           │
└──┬──────────────┬────────────┘
   │              │
┌──▼──┐      ┌──▼──┐
│Back │      │Back │
│end1 │      │end2 │
└──┬──┘      └──┬──┘
   │         │
   └────┬────┘
        │
   ┌────▼──────┐
   │  Database │
   │  Cluster  │
   └───────────┘
```

### 17.2 Caching Strategy

```
Frontend:
├─ HTTP caching (Cache-Control headers)
├─ Local state caching (React Query)
└─ Service worker for offline support

Backend:
├─ Database query caching (Redis)
├─ HTTP caching headers
└─ CDN for static assets

Database:
├─ Connection pooling
├─ Query result caching
└─ Index optimization
```

### 17.3 Microservices (Future)

```
Current (Phase II):
┌─────────────────┐
│  FastAPI Backend │
├─────────────────┤
│ Auth Service    │
│ Task Service    │
│ User Service    │
└─────────────────┘

Future (Phase III+):
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ Auth Microservice│  │ Task Microservice│  │ User Microservice│
├──────────────────┤  ├──────────────────┤  ├──────────────────┤
│ JWT generation  │  │ CRUD operations  │  │ Profile mgmt    │
│ Token refresh   │  │ Task filtering   │  │ User settings   │
│ User validation │  │ Task sharing     │  │ Preferences     │
└──────────────────┘  └──────────────────┘  └──────────────────┘
      ↓                    ↓                       ↓
   Auth DB             Tasks DB                Users DB
```

---

## 18. Documentation Standards

### 18.1 Code Documentation

```
Frontend Components:
├─ JSDoc comments on functions
├─ Prop type documentation
├─ Usage examples
└─ Edge cases documented

Backend Endpoints:
├─ Docstrings on all functions
├─ Parameter descriptions
├─ Return type documentation
├─ Exception documentation
└─ FastAPI auto-generates from docstrings

API Documentation:
├─ OpenAPI/Swagger (auto-generated from FastAPI)
└─ Postman collection

Architecture Documentation:
├─ diagrams explaining data flow
├─ sequence diagrams for workflows
└─ deployment guides
```

### 18.2 README Structure

```
Root README.md:
├─ Project overview
├─ Tech stack
├─ Getting started
├─ Project structure
├─ Architecture overview
└─ Contributing guide

apps/frontend/README.md:
├─ Frontend setup
├─ Available scripts
├─ Component structure
├─ Testing guide
└─ Deployment

apps/backend/README.md:
├─ Backend setup
├─ Database setup
├─ API endpoints
├─ Testing guide
└─ Deployment
```

---

## 19. Success Criteria

### 19.1 Architecture Success Criteria

- [ ] Clean separation of concerns (frontend, backend, database)
- [ ] Type-safe across all layers (TypeScript, Python hints)
- [ ] Stateless API (no server sessions)
- [ ] JWT token lifecycle working correctly
- [ ] All data flows documented with diagrams
- [ ] <100ms average API response time
- [ ] <3 second frontend page load time
- [ ] >95% uptime SLA ready

### 19.2 Integration Success Criteria

- [ ] Frontend and backend developed in parallel
- [ ] Shared types kept in sync
- [ ] All API contracts honored
- [ ] Mock API works for frontend development
- [ ] Real API seamlessly replaces mock API
- [ ] All E2E tests pass
- [ ] No authentication issues
- [ ] No CORS issues

### 19.3 Scalability Success Criteria

- [ ] Architecture supports 100+ concurrent users
- [ ] Database can handle 10,000+ tasks
- [ ] Requests remain <200ms at scale
- [ ] Horizontal scaling possible
- [ ] No single point of failure
- [ ] Monitoring and alerting in place

---

## 20. Document Metadata

**Document**: Phase II Full-Stack Architecture Plan
**Version**: 1.0
**Status**: READY FOR IMPLEMENTATION
**Date**: December 30, 2025
**Last Updated**: December 30, 2025

**Key Sections**:
- Monorepo structure and responsibilities
- Layered architecture
- Complete data flows with diagrams
- JWT authentication flow details
- Frontend-backend integration points
- Deployment and scalability
- Security architecture
- Testing strategy
- Monitoring and logging

**Total**: 20 sections, 50+ diagrams, 100+ detailed explanations

---

## Appendix A: Architecture Decision Log

```
ADL-001: Monorepo Structure
├─ Decision: Use monorepo for frontend and backend
├─ Rationale: Shared types, unified CI/CD
├─ Date: 2025-12-30
└─ Status: APPROVED

ADL-002: JWT vs Sessions
├─ Decision: Use JWT tokens
├─ Rationale: Stateless, scalable
├─ Date: 2025-12-30
└─ Status: APPROVED

ADL-003: REST vs GraphQL
├─ Decision: REST API
├─ Rationale: Simple, standard, suitable for CRUD
├─ Date: 2025-12-30
└─ Status: APPROVED

ADL-004: Frontend State Management
├─ Decision: Context API + hooks
├─ Rationale: Simple, built-in to React
├─ Date: 2025-12-30
└─ Status: APPROVED

ADL-005: Database: PostgreSQL
├─ Decision: PostgreSQL with Neon
├─ Rationale: Relational, ACID, managed hosting
├─ Date: 2025-12-30
└─ Status: APPROVED
```

---

## Appendix B: Quick Architecture Reference

```
Request Path:
Browser → Next.js → API Client → Axios → Backend → Database

Token Lifecycle:
Login → Get tokens → Store locally → Include in headers →
Verify on backend → Refresh if needed → Logout → Clear tokens

Component Hierarchy:
App Layout → Auth/Dashboard → Pages → Components → Child Components

Data Flow:
User Action → Service Call → API Request → Backend Processing →
Database Query → Response → Service Processing → State Update →
Component Re-render → UI Update

Authentication:
Credentials → Generate JWT → Store tokens → API headers →
Verify JWT → Get user → Process request → Return response
```

---

## Appendix C: Key Files and Their Purposes

```
Frontend:
├─ app/layout.tsx: Root layout wrapper
├─ app/api/[...proxy].ts: Backend API proxy (optional)
├─ context/AuthContext.tsx: Auth state provider
├─ services/api.ts: HTTP client configuration
├─ services/tasks.ts: Task API calls
├─ hooks/useAuth.ts: Auth logic hook
├─ hooks/useTask.ts: Task logic hook
└─ utils/jwt.ts: JWT parsing and validation

Backend:
├─ main.py: FastAPI app initialization
├─ config.py: Configuration and settings
├─ database.py: Database connection setup
├─ security.py: JWT verification logic
├─ api/endpoints/auth.py: Auth routes
├─ api/endpoints/tasks.py: Task routes
├─ services/auth.py: Auth business logic
├─ services/task.py: Task business logic
├─ models/user.py: Database user model
└─ models/task.py: Database task model
```

---

**END OF ARCHITECTURE PLAN**
