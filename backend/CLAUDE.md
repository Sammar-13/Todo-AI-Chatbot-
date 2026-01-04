# CLAUDE.md - Backend Development Guide

## Overview
This document provides guidance for backend development and AI assistance in the Hackathon Todo Application.

## Backend Stack

### Recommended Technologies
- **Runtime**: Node.js 18+ or Python 3.10+
- **Framework**: Express.js, FastAPI, or NestJS
- **Database**: PostgreSQL 14+ or MongoDB 5+
- **ORM/ODM**: Sequelize, TypeORM, SQLAlchemy, or Mongoose
- **Testing**: Jest, pytest, or Mocha
- **API Documentation**: Swagger/OpenAPI

## Getting Started

### Prerequisites
- Node.js 18+ or Python 3.10+
- PostgreSQL or MongoDB
- Package manager (npm, yarn, or pip)
- Code editor (VS Code recommended)
- Git configured
- Postman or similar API testing tool

### Project Setup (Node.js)
```bash
# Clone repository
git clone <repository-url>
cd hackathon-todo/backend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Run database migrations
npm run db:migrate

# Start development server
npm run dev

# Run tests
npm test
```

### Project Setup (Python)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run database migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

## Development Guidelines

### Before Development
1. Read `specs/phase2/specify.md` for API requirements
2. Review `specs/architecture.md` for system design
3. Understand authentication flow
4. Check database schema
5. Review error handling standards

### During Development
1. Implement endpoints following specification
2. Write tests alongside code
3. Validate all inputs
4. Handle errors gracefully
5. Document API changes

### Code Structure (Node.js)
```
backend/src/
├── config/              # Configuration files
├── controllers/         # Route handlers
├── services/            # Business logic
├── models/              # Database models
├── middleware/          # Express middleware
├── routes/              # Route definitions
├── validators/          # Input validation
├── utils/               # Utility functions
├── types/               # TypeScript interfaces
└── index.ts             # Entry point
```

### Code Structure (Python)
```
backend/
├── config/              # Configuration
├── app/
│   ├── models/          # Database models
│   ├── routes/          # API routes
│   ├── services/        # Business logic
│   ├── validators/      # Input validation
│   └── utils/           # Utilities
├── tests/               # Tests
├── migrations/          # Database migrations
└── manage.py            # Management commands
```

## REST API Development

### Endpoint Implementation Pattern (Node.js)
```typescript
// routes/todos.ts
import { Router, Request, Response } from 'express';
import { authMiddleware } from '@/middleware/auth';
import { todoService } from '@/services/todoService';
import { validateTodo } from '@/validators/todoValidator';

const router = Router();

// Get all todos
router.get('/', authMiddleware, async (req: Request, res: Response) => {
  try {
    const todos = await todoService.getUserTodos(req.user.id);
    res.json({ success: true, data: todos });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: { code: 'SERVER_ERROR', message: 'Failed to fetch todos' }
    });
  }
});

// Create todo
router.post('/', authMiddleware, async (req: Request, res: Response) => {
  try {
    // Validate input
    const validation = validateTodo(req.body);
    if (!validation.valid) {
      return res.status(400).json({
        success: false,
        error: { code: 'VALIDATION_ERROR', details: validation.errors }
      });
    }

    // Create todo
    const todo = await todoService.createTodo(req.user.id, req.body);
    res.status(201).json({ success: true, data: todo });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: { code: 'SERVER_ERROR', message: 'Failed to create todo' }
    });
  }
});

export default router;
```

### Service Layer Pattern
```typescript
// services/todoService.ts
import { Todo } from '@/models/Todo';
import { NotFoundError, UnauthorizedError } from '@/utils/errors';

export const todoService = {
  async getUserTodos(userId: string): Promise<Todo[]> {
    return await Todo.find({ user_id: userId, is_deleted: false });
  },

  async getTodoById(id: string, userId: string): Promise<Todo> {
    const todo = await Todo.findOne({ id, user_id: userId });
    if (!todo) throw new NotFoundError('Todo not found');
    return todo;
  },

  async createTodo(userId: string, data: CreateTodoRequest): Promise<Todo> {
    const todo = new Todo({
      ...data,
      user_id: userId,
      status: 'pending'
    });
    return await todo.save();
  },

  async updateTodo(
    id: string,
    userId: string,
    updates: Partial<Todo>
  ): Promise<Todo> {
    const todo = await this.getTodoById(id, userId);
    Object.assign(todo, updates);
    return await todo.save();
  },

  async deleteTodo(id: string, userId: string): Promise<void> {
    const todo = await this.getTodoById(id, userId);
    await todo.delete();
  }
};
```

## Authentication & Authorization

### JWT Implementation
```typescript
// utils/jwt.ts
import jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';
const REFRESH_SECRET = process.env.REFRESH_SECRET || 'refresh-secret';

export const jwtUtils = {
  generateToken(userId: string, expiresIn = '24h'): string {
    return jwt.sign({ userId }, JWT_SECRET, { expiresIn });
  },

  generateRefreshToken(userId: string): string {
    return jwt.sign({ userId }, REFRESH_SECRET, { expiresIn: '7d' });
  },

  verifyToken(token: string): { userId: string } {
    try {
      return jwt.verify(token, JWT_SECRET) as { userId: string };
    } catch (error) {
      throw new Error('Invalid token');
    }
  },

  refreshToken(refreshToken: string): string {
    try {
      const decoded = jwt.verify(refreshToken, REFRESH_SECRET) as { userId: string };
      return this.generateToken(decoded.userId);
    } catch (error) {
      throw new Error('Invalid refresh token');
    }
  }
};
```

### Auth Middleware
```typescript
// middleware/auth.ts
import { Request, Response, NextFunction } from 'express';
import { jwtUtils } from '@/utils/jwt';

export const authMiddleware = (
  req: Request & { user?: { id: string } },
  res: Response,
  next: NextFunction
) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) {
      return res.status(401).json({
        success: false,
        error: { code: 'UNAUTHORIZED', message: 'Missing token' }
      });
    }

    const decoded = jwtUtils.verifyToken(token);
    req.user = { id: decoded.userId };
    next();
  } catch (error) {
    res.status(401).json({
      success: false,
      error: { code: 'UNAUTHORIZED', message: 'Invalid token' }
    });
  }
};
```

## Database

### Model Definition
```typescript
// models/Todo.ts
import { DataTypes, Model } from 'sequelize';
import { sequelize } from '@/config/database';

export interface Todo {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  status: 'pending' | 'completed' | 'archived';
  priority: 'low' | 'medium' | 'high';
  due_date?: Date;
  created_at: Date;
  updated_at: Date;
}

export const TodoModel = sequelize.define<Model<Todo>>('Todo', {
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true
  },
  user_id: {
    type: DataTypes.UUID,
    allowNull: false
  },
  title: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: { len: [3, 255] }
  },
  description: DataTypes.TEXT,
  status: {
    type: DataTypes.ENUM('pending', 'completed', 'archived'),
    defaultValue: 'pending'
  },
  priority: {
    type: DataTypes.ENUM('low', 'medium', 'high'),
    defaultValue: 'medium'
  },
  due_date: DataTypes.DATE,
  created_at: {
    type: DataTypes.DATE,
    defaultValue: DataTypes.NOW
  },
  updated_at: {
    type: DataTypes.DATE,
    defaultValue: DataTypes.NOW
  }
});

// Indexes for performance
TodoModel.addIndex(['user_id']);
TodoModel.addIndex(['status']);
TodoModel.addIndex(['due_date']);
```

### Database Migrations
```typescript
// migrations/001-create-users.ts
export const up = async (queryInterface: any) => {
  await queryInterface.createTable('users', {
    id: {
      type: 'UUID',
      primaryKey: true,
      defaultValue: 'gen_random_uuid()'
    },
    email: {
      type: 'VARCHAR(255)',
      unique: true,
      allowNull: false
    },
    password_hash: {
      type: 'VARCHAR(255)',
      allowNull: false
    },
    name: {
      type: 'VARCHAR(255)',
      allowNull: false
    },
    created_at: {
      type: 'TIMESTAMP',
      defaultValue: 'now()'
    },
    updated_at: {
      type: 'TIMESTAMP',
      defaultValue: 'now()'
    }
  });
};

export const down = async (queryInterface: any) => {
  await queryInterface.dropTable('users');
};
```

## Validation

### Input Validation
```typescript
// validators/todoValidator.ts
import { CreateTodoRequest } from '@/types';

export const validateTodo = (data: unknown) => {
  const errors: { [key: string]: string[] } = {};

  if (!data || typeof data !== 'object') {
    return { valid: false, errors: { general: ['Invalid request'] } };
  }

  const todo = data as any;

  // Validate title
  if (!todo.title || typeof todo.title !== 'string') {
    errors.title = ['Title is required and must be a string'];
  } else if (todo.title.length < 3 || todo.title.length > 255) {
    errors.title = ['Title must be between 3 and 255 characters'];
  }

  // Validate priority
  if (todo.priority && !['low', 'medium', 'high'].includes(todo.priority)) {
    errors.priority = ['Priority must be low, medium, or high'];
  }

  // Validate due date
  if (todo.due_date) {
    const date = new Date(todo.due_date);
    if (isNaN(date.getTime())) {
      errors.due_date = ['Due date must be a valid ISO date'];
    }
  }

  return {
    valid: Object.keys(errors).length === 0,
    errors
  };
};
```

## Error Handling

### Custom Error Classes
```typescript
// utils/errors.ts
export class AppError extends Error {
  constructor(
    public code: string,
    public statusCode: number,
    message: string
  ) {
    super(message);
  }
}

export class NotFoundError extends AppError {
  constructor(message = 'Not found') {
    super('NOT_FOUND', 404, message);
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super('UNAUTHORIZED', 401, message);
  }
}

export class ValidationError extends AppError {
  constructor(public details: Record<string, string[]> = {}) {
    super('VALIDATION_ERROR', 400, 'Validation failed');
  }
}
```

### Global Error Handler
```typescript
// middleware/errorHandler.ts
import { Request, Response, NextFunction } from 'express';
import { AppError } from '@/utils/errors';

export const errorHandler = (
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  console.error('Error:', error);

  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      success: false,
      error: {
        code: error.code,
        message: error.message,
        details: 'details' in error ? error.details : undefined
      }
    });
  }

  // Generic error
  res.status(500).json({
    success: false,
    error: {
      code: 'SERVER_ERROR',
      message: 'An unexpected error occurred'
    }
  });
};
```

## Testing

### Unit Tests
```typescript
// __tests__/services/todoService.test.ts
import { todoService } from '@/services/todoService';
import { TodoModel } from '@/models/Todo';

jest.mock('@/models/Todo');

describe('todoService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('createTodo', () => {
    it('should create a todo with valid data', async () => {
      const mockData = {
        id: '123',
        user_id: 'user-1',
        title: 'Test Todo',
        status: 'pending'
      };

      (TodoModel.create as jest.Mock).mockResolvedValue(mockData);

      const result = await todoService.createTodo('user-1', {
        title: 'Test Todo'
      });

      expect(result).toEqual(mockData);
      expect(TodoModel.create).toHaveBeenCalled();
    });

    it('should throw error for invalid title', async () => {
      await expect(
        todoService.createTodo('user-1', { title: 'ab' })
      ).rejects.toThrow();
    });
  });
});
```

### Integration Tests
```typescript
// __tests__/routes/todos.test.ts
import request from 'supertest';
import app from '@/index';
import { jwtUtils } from '@/utils/jwt';

describe('POST /api/v1/todos', () => {
  it('should create a todo with valid data', async () => {
    const token = jwtUtils.generateToken('user-1');

    const response = await request(app)
      .post('/api/v1/todos')
      .set('Authorization', `Bearer ${token}`)
      .send({
        title: 'Test Todo',
        priority: 'high'
      });

    expect(response.status).toBe(201);
    expect(response.body.success).toBe(true);
    expect(response.body.data.title).toBe('Test Todo');
  });

  it('should return 401 without token', async () => {
    const response = await request(app)
      .post('/api/v1/todos')
      .send({ title: 'Test Todo' });

    expect(response.status).toBe(401);
  });
});
```

## Performance Optimization

### Query Optimization
```typescript
// Optimize: Use select to fetch only needed columns
const todos = await Todo.findAll({
  where: { user_id: userId },
  attributes: ['id', 'title', 'status'],
  limit: 20
});

// Optimize: Use eager loading to avoid N+1
const users = await User.findAll({
  include: [{
    association: 'todos',
    attributes: ['id', 'title']
  }]
});

// Optimize: Use indexes
// CREATE INDEX idx_todos_user_status ON todos(user_id, status);
```

### Caching
```typescript
// utils/cache.ts
import redis from 'redis';

const client = redis.createClient();

export const cacheService = {
  async get<T>(key: string): Promise<T | null> {
    const data = await client.get(key);
    return data ? JSON.parse(data) : null;
  },

  async set(key: string, value: unknown, ttl = 3600): Promise<void> {
    await client.setex(key, ttl, JSON.stringify(value));
  },

  async delete(key: string): Promise<void> {
    await client.del(key);
  }
};
```

## Security

### Password Hashing
```typescript
import bcrypt from 'bcrypt';

export const passwordUtils = {
  async hash(password: string): Promise<string> {
    return await bcrypt.hash(password, 10);
  },

  async compare(password: string, hash: string): Promise<boolean> {
    return await bcrypt.compare(password, hash);
  }
};
```

### Input Sanitization
```typescript
import sanitizeHtml from 'sanitize-html';

export const sanitize = (input: string): string => {
  return sanitizeHtml(input, {
    allowedTags: [],
    allowedAttributes: {}
  });
};
```

### Rate Limiting
```typescript
import rateLimit from 'express-rate-limit';

export const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests, please try again later'
});
```

## Using AI for Backend Development

### Good Use Cases
- Endpoint implementation
- Service layer code
- Database schema design
- Error handling
- Test code generation
- Documentation

### Best Practices
1. Provide specification details
2. Include existing code patterns
3. Ask for security review
4. Request error handling
5. Ask for test suggestions

### Red Flags
- AI code without review
- Skipping input validation
- Missing error handling
- No authentication checks
- Hardcoded secrets

## Deployment

### Build and Test
```bash
# Run all tests
npm test

# Build for production
npm run build

# Run linting
npm run lint

# Check for vulnerabilities
npm audit
```

### Environment Variables
```bash
# Create .env.production
DATABASE_URL=postgresql://user:pass@host/db
JWT_SECRET=your-secret-key
NODE_ENV=production
PORT=3001
```

## Monitoring

### Logging
```typescript
import logger from 'winston';

logger.info('Todo created', { userId, todoId });
logger.error('Database error', { error: err });
```

### Health Check
```typescript
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date(),
    uptime: process.uptime()
  });
});
```

## Resources

### Documentation
- [Express.js Documentation](https://expressjs.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [NestJS Documentation](https://docs.nestjs.com)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Tools
- Postman (API testing)
- DBeaver (Database management)
- VS Code
- Nodemon (Development)

## Common Patterns

### Async Error Wrapper
```typescript
export const asyncHandler = (fn: Function) => (req: Request, res: Response, next: NextFunction) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

// Usage
router.get('/', asyncHandler(async (req, res) => {
  const data = await someAsyncOperation();
  res.json(data);
}));
```

## FAQ

**Q: How do I handle async errors?**
A: Use try-catch or async error wrapper middleware.

**Q: How do I validate input?**
A: Create validators with clear error messages, return 400 with details.

**Q: How do I secure the API?**
A: Use JWT auth, validate input, use HTTPS, implement rate limiting, hash passwords.

**Q: How do I optimize database queries?**
A: Use indexes, eager loading, select specific columns, paginate results.

**Q: Can AI help with implementation?**
A: Yes, but review thoroughly, test before committing, ensure security and spec compliance.

---

Last Updated: December 30, 2025
Version: 1.0.0
