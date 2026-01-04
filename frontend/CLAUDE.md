# CLAUDE.md - Frontend Development Guide

## Overview
This document provides guidance for frontend development and AI assistance in the Hackathon Todo Application.

## Frontend Stack

### Recommended Technologies
- **Framework**: React 18+, Vue 3+, or Angular 16+
- **Build Tool**: Webpack 5+ or Vite 4+
- **Styling**: Tailwind CSS, Material-UI, or vanilla CSS
- **State Management**: Redux, Vuex, or Context API
- **Testing**: Jest, Vitest, React Testing Library
- **E2E Testing**: Cypress or Playwright

## Getting Started

### Prerequisites
- Node.js 18+
- npm or yarn package manager
- Code editor (VS Code recommended)
- Git configured

### Project Setup
```bash
# Clone repository
git clone <repository-url>
cd hackathon-todo/frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

## Development Guidelines

### Before Development
1. Read `specs/phase3/specify.md` for requirements
2. Review `specs/architecture.md` for system design
3. Check design system if available
4. Understand API contract from `specs/phase2/specify.md`

### During Development
1. Create components matching specification
2. Follow file structure conventions
3. Write tests alongside code
4. Maintain accessibility standards
5. Test responsive design

### Code Structure
```
frontend/src/
├── components/          # Reusable components
│   ├── common/         # Shared components
│   └── features/       # Feature-specific
├── pages/              # Page components
├── services/           # API and utilities
├── hooks/              # Custom React hooks
├── context/            # Context/state management
├── styles/             # Global styles
├── types/              # TypeScript types
└── App.tsx             # Root component
```

## Component Development

### Component Template
```tsx
// components/MyComponent.tsx
import React from 'react';
import { ComponentProps } from '@/types';
import styles from './MyComponent.module.css';

interface Props {
  title: string;
  onAction: () => void;
}

export const MyComponent: React.FC<Props> = ({ title, onAction }) => {
  return (
    <div className={styles.container}>
      <h2>{title}</h2>
      <button onClick={onAction}>Action</button>
    </div>
  );
};

export default MyComponent;
```

### Component Checklist
- ✓ Props properly typed
- ✓ Accessible (ARIA labels, semantic HTML)
- ✓ Responsive design
- ✓ Unit tests included
- ✓ Storybook stories (if applicable)
- ✓ Error boundaries
- ✓ Loading states
- ✓ Documentation comments

## State Management

### Context/Redux Pattern
```tsx
// context/TodoContext.tsx
import React, { createContext, useReducer } from 'react';

interface TodoState {
  todos: Todo[];
  loading: boolean;
  error: string | null;
}

export const TodoContext = createContext<TodoState | undefined>(undefined);

export const TodoProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(todoReducer, initialState);
  return (
    <TodoContext.Provider value={state}>
      {children}
    </TodoContext.Provider>
  );
};

export const useTodos = () => {
  const context = useContext(TodoContext);
  if (!context) throw new Error('useTodos must be used within TodoProvider');
  return context;
};
```

## API Integration

### Service Pattern
```typescript
// services/todoService.ts
import { apiClient } from '@/utils/apiClient';
import { Todo, CreateTodoRequest } from '@/types';

export const todoService = {
  async getTodos(): Promise<Todo[]> {
    const response = await apiClient.get('/todos');
    return response.data;
  },

  async createTodo(data: CreateTodoRequest): Promise<Todo> {
    const response = await apiClient.post('/todos', data);
    return response.data;
  },

  async updateTodo(id: string, data: Partial<Todo>): Promise<Todo> {
    const response = await apiClient.put(`/todos/${id}`, data);
    return response.data;
  },

  async deleteTodo(id: string): Promise<void> {
    await apiClient.delete(`/todos/${id}`);
  }
};
```

### Using Services in Components
```tsx
import { useEffect, useState } from 'react';
import { todoService } from '@/services/todoService';
import { Todo } from '@/types';

export const TodoList: React.FC = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadTodos = async () => {
      try {
        setLoading(true);
        const data = await todoService.getTodos();
        setTodos(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load todos');
      } finally {
        setLoading(false);
      }
    };

    loadTodos();
  }, []);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <ul>
      {todos.map(todo => (
        <li key={todo.id}>{todo.title}</li>
      ))}
    </ul>
  );
};
```

## Styling

### CSS Structure
```css
/* styles/globals.css */
:root {
  --color-primary: #007bff;
  --color-secondary: #6c757d;
  --spacing-unit: 8px;
  --border-radius: 4px;
}

/* Component styles */
.container {
  display: flex;
  gap: var(--spacing-unit);
  padding: var(--spacing-unit);
  border-radius: var(--border-radius);
}

.container:hover {
  background-color: var(--color-primary);
}
```

### Responsive Design
```css
/* Mobile first */
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

/* Tablet and up */
@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

## Testing

### Unit Tests
```typescript
// __tests__/components/MyComponent.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MyComponent } from '@/components/MyComponent';

describe('MyComponent', () => {
  it('renders with title', () => {
    render(<MyComponent title="Test" onAction={jest.fn()} />);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('calls onAction when button is clicked', async () => {
    const mockAction = jest.fn();
    const user = userEvent.setup();

    render(<MyComponent title="Test" onAction={mockAction} />);
    await user.click(screen.getByRole('button'));

    expect(mockAction).toHaveBeenCalled();
  });
});
```

### Test Checklist
- ✓ Component renders correctly
- ✓ Props affect rendering
- ✓ User interactions work
- ✓ Error states handled
- ✓ Loading states shown
- ✓ API calls mocked
- ✓ Accessibility verified

## Accessibility

### WCAG 2.1 Level AA Standards

#### Semantic HTML
```tsx
// GOOD
<button onClick={handleClick}>Click me</button>
<nav aria-label="Main">...</nav>
<main>
  <section aria-label="Todo List">...</section>
</main>

// AVOID
<div onClick={handleClick} role="button">Click me</div>
<div>...</div>
```

#### ARIA Labels
```tsx
// GOOD
<input aria-label="Search todos" type="search" />
<button aria-label="Close dialog">×</button>
<div role="alert">{error}</div>

// AVOID
<input type="search" />
<button>×</button>
```

#### Color Contrast
```css
/* GOOD - Contrast ratio >= 4.5:1 */
.text {
  color: #000000;  /* Black */
  background-color: #ffffff;  /* White */
}

/* AVOID - Contrast ratio < 4.5:1 */
.text {
  color: #999999;  /* Gray */
  background-color: #f5f5f5;  /* Light gray */
}
```

### Testing Accessibility
```bash
# Run axe accessibility tests
npm run test:a11y

# Manual testing with screen reader
# - Use NVDA (Windows) or VoiceOver (Mac)
# - Test keyboard navigation (Tab, Enter, Escape)
# - Verify heading hierarchy
```

## Performance

### Code Splitting
```tsx
// pages/index.tsx
import { Suspense, lazy } from 'react';

const TodoList = lazy(() => import('@/pages/TodoList'));
const Profile = lazy(() => import('@/pages/Profile'));

export const App = () => (
  <Suspense fallback={<LoadingSpinner />}>
    {/* Routes with lazy components */}
  </Suspense>
);
```

### Image Optimization
```tsx
// GOOD - Optimized image
import Image from 'next/image';  // if using Next.js

<Image
  src="/todos.jpg"
  alt="Todo list"
  width={800}
  height={600}
  quality={75}
  loading="lazy"
/>

// Or with regular img
<img
  src="/todos.webp"
  alt="Todo list"
  loading="lazy"
  srcSet="/todos-sm.webp 480w, /todos-lg.webp 1024w"
  sizes="(max-width: 480px) 100vw, 50vw"
/>
```

### Performance Targets
- Lighthouse score: ≥85
- Time to Interactive: <3s
- First Contentful Paint: <1s
- Cumulative Layout Shift: <0.1

## Error Handling

### Error Boundary
```tsx
// components/ErrorBoundary.tsx
import React, { ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught:', error, errorInfo);
    // Send to error tracking service
  }

  render() {
    if (this.state.hasError) {
      return <ErrorPage error={this.state.error} />;
    }

    return this.props.children;
  }
}
```

### User Feedback
```tsx
// Toasts for user feedback
const showToast = (message: string, type: 'success' | 'error' | 'info') => {
  // Show toast notification
};

// Usage
try {
  await todoService.createTodo(data);
  showToast('Todo created successfully', 'success');
} catch (error) {
  showToast('Failed to create todo', 'error');
}
```

## Debugging

### Development Tools
```bash
# Start dev server with source maps
npm run dev

# Debug in Chrome DevTools
# 1. Open Chrome DevTools (F12)
# 2. Go to Sources tab
# 3. Set breakpoints in code
# 4. Step through execution

# React DevTools extension
# Install from Chrome Web Store
# View component hierarchy and state
```

### Logging
```typescript
// utils/logger.ts
export const logger = {
  info: (message: string, data?: unknown) =>
    console.log(`[INFO] ${message}`, data),
  error: (message: string, error?: Error) =>
    console.error(`[ERROR] ${message}`, error),
  warn: (message: string, data?: unknown) =>
    console.warn(`[WARN] ${message}`, data),
};
```

## Using AI for Frontend Development

### Good Use Cases
- Component boilerplate generation
- Form implementation
- API integration code
- Styling help
- Test code generation
- Documentation

### Best Practices
1. Provide current component code
2. Reference specification requirements
3. Ask for accessibility improvements
4. Review generated code thoroughly
5. Test before committing

### Red Flags
- AI-generated code without review
- Skipping component testing
- Ignoring accessibility
- Hardcoding values
- Missing error handling

## Build and Deployment

### Production Build
```bash
# Build for production
npm run build

# Analyze bundle
npm run build:analyze

# Test production build locally
npm run preview
```

### Deployment Checklist
- ✓ Tests passing
- ✓ Build successful
- ✓ No console errors
- ✓ Accessibility verified
- ✓ Performance acceptable
- ✓ Environment variables configured
- ✓ API endpoints verified

## Resources

### Documentation
- [React Documentation](https://react.dev)
- [Vue Documentation](https://vuejs.org)
- [Angular Documentation](https://angular.io)
- [MDN Web Docs](https://developer.mozilla.org)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

### Tools
- VS Code
- Chrome DevTools
- React DevTools
- Lighthouse
- axe DevTools

## Common Patterns

### Using Hooks
```tsx
// Custom hook for data fetching
const useFetch = <T,>(url: string) => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetch = async () => {
      try {
        const response = await fetch(url);
        setData(await response.json());
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };
    fetch();
  }, [url]);

  return { data, loading, error };
};
```

## FAQ

**Q: How do I handle API errors?**
A: Use try-catch blocks and error boundaries. Show user-friendly error messages.

**Q: How do I ensure accessibility?**
A: Use semantic HTML, test with screen readers, verify color contrast, support keyboard navigation.

**Q: How do I optimize performance?**
A: Code split by routes, lazy load images, memoize expensive computations, profile with Lighthouse.

**Q: How do I test components?**
A: Write unit tests with React Testing Library, E2E tests with Cypress/Playwright.

**Q: Can I use AI to generate components?**
A: Yes, but review thoroughly, test before committing, ensure accessibility and spec compliance.

---

Last Updated: December 30, 2025
Version: 1.0.0
