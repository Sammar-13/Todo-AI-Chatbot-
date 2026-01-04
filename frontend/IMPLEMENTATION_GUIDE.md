# Frontend Implementation Guide - Complete Code Snippets

This document provides all remaining component and page code that needs to be created to complete the Phase 3 frontend implementation.

## Already Generated Files

The following files have been generated and are ready to use:

### Configuration Files
- `package.json` - Dependencies and scripts
- `tsconfig.json` - TypeScript configuration
- `tailwind.config.ts` - Tailwind CSS configuration
- `next.config.js` - Next.js configuration
- `postcss.config.js` - PostCSS configuration
- `.env.local.example` - Environment variables template

### Type Definitions
- `src/types/index.ts` - All TypeScript types and interfaces

### Services
- `src/services/auth.ts` - Authentication API service
- `src/services/tasks.ts` - Tasks API service
- `src/services/users.ts` - Users API service
- `src/utils/api.ts` - API client with token management

### Context/State Management
- `src/context/AuthContext.tsx` - Auth state provider
- `src/context/TaskContext.tsx` - Task state provider
- `src/context/UIContext.tsx` - UI state provider

### Hooks
- `src/hooks/useAuth.ts` - Auth context hook
- `src/hooks/useTask.ts` - Task context hook
- `src/hooks/useUI.ts` - UI context hook
- `src/hooks/useFetch.ts` - Data fetching hook
- `src/hooks/useLocalStorage.ts` - LocalStorage hook

### Utilities
- `src/utils/api.ts` - HTTP client
- `src/utils/token.ts` - JWT token utilities
- `src/utils/format.ts` - Data formatting utilities
- `src/utils/validation.ts` - Form validation schemas and functions

### Common Components
- `src/components/Common/Modal.tsx` - Modal dialog
- `src/components/Common/Toast.tsx` - Toast notifications
- `src/components/Common/Loading.tsx` - Spinners and skeletons
- `src/components/Common/ErrorBoundary.tsx` - Error boundary

## Remaining Components to Create

### 1. Common UI Components

#### Button Component
File: `src/components/Common/Button.tsx`
- Variants: primary, secondary, danger
- Sizes: sm, md, lg
- States: loading, disabled
- Full width option

#### Input Component
File: `src/components/Common/Input.tsx`
- Text, email, password types
- Label and error message
- Validation feedback
- Required indicator

#### Badge Component
File: `src/components/Common/Badge.tsx`
- Status badges
- Priority badges
- Dismissible option

### 2. Layout Components

#### Navigation Component
File: `src/components/Layout/Navigation.tsx`
- Logo and branding
- Navigation links
- User menu with profile/logout
- Mobile responsive hamburger menu

#### Sidebar Component
File: `src/components/Layout/Sidebar.tsx`
- Navigation links with icons
- Active link highlighting
- Collapsible on mobile
- User quick actions

#### Footer Component
File: `src/components/Layout/Footer.tsx`
- Copyright information
- Links
- Social media (optional)

### 3. Auth Components

#### LoginForm Component
File: `src/components/Auth/LoginForm.tsx`
- Email and password inputs
- Remember me checkbox
- Login button with loading state
- Error display
- Link to signup

#### SignUpForm Component
File: `src/components/Auth/SignUpForm.tsx`
- Email, full name, password inputs
- Password confirmation
- Terms & conditions checkbox
- Password strength indicator
- Signup button with loading state
- Error display
- Link to login

#### ProtectedRoute Component
File: `src/components/Auth/ProtectedRoute.tsx`
- Check authentication
- Redirect to login if not authenticated
- Show loading state

### 4. Task Components

#### TaskCard Component
File: `src/components/Tasks/TaskCard.tsx`
- Task title
- Description (truncated)
- Status and priority badges
- Due date display
- Quick action buttons (complete, edit, delete)
- Click to navigate to detail
- Responsive styling

#### TaskList Component
File: `src/components/Tasks/TaskList.tsx`
- Map tasks to TaskCard
- Empty state message
- Loading skeleton
- Pagination controls
- Task statistics (X pending, Y complete)
- Refresh button

#### TaskForm Component
File: `src/components/Tasks/TaskForm.tsx`
- Title input (required)
- Description textarea (optional)
- Priority selector
- Due date picker
- Submit and cancel buttons
- Form validation
- Loading state
- Error display
- Pre-fill when editing

#### TaskFilter Component
File: `src/components/Tasks/TaskFilter.tsx`
- Status filter (All, Pending, Completed)
- Priority filter
- Sort selector
- Order selector (asc/desc)
- Search input
- Clear filters button
- Active filter visual feedback

#### TaskStats Component
File: `src/components/Tasks/TaskStats.tsx`
- Total tasks count
- Pending tasks count
- Completed tasks count
- Completion percentage
- Visual indicators

### 5. Pages

#### Root Layout
File: `src/app/layout.tsx`
- Metadata
- Providers (Auth, Task, UI)
- Global styles
- Font configuration
- Error boundary

#### Root Page (Landing)
File: `src/app/page.tsx`
- Hero section
- Feature highlights
- Call-to-action buttons
- Footer

#### Auth Layout
File: `src/app/(auth)/layout.tsx`
- No sidebar
- Centered content
- Auth-specific styling

#### Login Page
File: `src/app/(auth)/login/page.tsx`
- Render LoginForm
- Redirect if authenticated
- Link to signup
- Error handling

#### Signup Page
File: `src/app/(auth)/signup/page.tsx`
- Render SignUpForm
- Redirect if authenticated
- Link to login
- Error handling

#### Dashboard Layout
File: `src/app/(dashboard)/layout.tsx`
- Navigation component
- Sidebar component
- Main content area
- Protected route wrapper
- Responsive layout

#### Dashboard Home
File: `src/app/(dashboard)/page.tsx`
- Welcome message
- Task statistics
- Quick actions
- Recent tasks list
- Create task button

#### Todos List Page
File: `src/app/(dashboard)/todos/page.tsx`
- Task list display
- Filters and sorting
- Search functionality
- Pagination
- Create task modal/form
- Empty state

#### Todo Detail Page
File: `src/app/(dashboard)/todos/[id]/page.tsx`
- Load task by ID
- Display full details
- Edit form
- Mark complete/pending toggle
- Delete button with confirmation
- Back navigation
- Not found state
- Error state

#### Settings Page
File: `src/app/(dashboard)/settings/page.tsx`
- Profile information display
- Edit profile form
- Change password form
- Notification preferences
- Theme selector
- Delete account section
- Confirmation dialogs

#### Tasks Overview Page
File: `src/app/(dashboard)/tasks/page.tsx`
- Alternative tasks view
- Statistics dashboard
- Filters and controls
- Task performance metrics

## Implementation Priority

1. **High Priority** (Core functionality):
   - Root Layout with Providers
   - Protected Route logic
   - Navigation and Sidebar
   - LoginForm and SignUpForm
   - TaskCard, TaskList, TaskForm, TaskFilter
   - All dashboard pages

2. **Medium Priority** (Enhanced UX):
   - Button, Input, Badge components
   - Task statistics and analytics
   - Error boundary integration
   - Loading states

3. **Low Priority** (Polish):
   - Footer component
   - Additional page variations
   - Animations and transitions
   - Performance optimizations

## Code Generation Template

Each component should follow this structure:

```typescript
/**
 * Component Name
 * Brief description
 * Task: XX-XXX (if from spec)
 */

'use client'

import React from 'react'
import type { [Props] } from '@/types'

interface [ComponentName]Props {
  // Props definition
}

export function [ComponentName]({ ... }: [ComponentName]Props) {
  // Component implementation

  return (
    // JSX
  )
}

export default [ComponentName]
```

## Tailwind CSS Patterns

### Button Variants
```typescript
const buttonClasses = {
  primary: 'bg-primary-500 hover:bg-primary-600 text-white',
  secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-800',
  danger: 'bg-red-500 hover:bg-red-600 text-white',
}
```

### Responsive Classes
```typescript
// Mobile first
className="w-full md:w-1/2 lg:w-1/3"
className="flex flex-col md:flex-row"
```

### Dark Mode
```typescript
className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
```

## Testing Considerations

Each component should have:
- Unit tests for logic
- Integration tests for API calls
- E2E tests for user workflows
- Accessibility tests

## Performance Optimization

- Code splitting by route (Next.js automatic)
- Lazy loading components with React.lazy
- Image optimization with next/image
- CSS optimization with Tailwind
- Bundle analysis

## Accessibility Checklist

For each component:
- [ ] Semantic HTML
- [ ] ARIA labels where needed
- [ ] Keyboard navigation support
- [ ] Focus management
- [ ] Color contrast (4.5:1 for text)
- [ ] Touch targets (44x44px minimum)
- [ ] Screen reader tested

## Security Best Practices

- [ ] CSRF protection
- [ ] XSS prevention
- [ ] Input sanitization
- [ ] Secure token storage
- [ ] HTTPS enforcement
- [ ] Content Security Policy

## Next Steps After Generation

1. Install dependencies: `npm install`
2. Create remaining components using provided templates
3. Run `npm run type-check` to verify TypeScript
4. Run `npm run dev` to start development server
5. Test all pages and components
6. Add unit and E2E tests
7. Performance optimization
8. Accessibility audit
9. Security review
10. Production build and deployment

## Useful Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)
- [Web Accessibility](https://www.w3.org/WAI/)

## Support Files

- Complete type definitions: `src/types/index.ts`
- API client documentation: `src/utils/api.ts`
- Validation schemas: `src/utils/validation.ts`
- Format utilities: `src/utils/format.ts`
- Token utilities: `src/utils/token.ts`

---

**Status**: Phase 3 Core Infrastructure Complete
**Remaining**: Components and Pages Implementation
**Estimated Time**: 2-3 days for full implementation
