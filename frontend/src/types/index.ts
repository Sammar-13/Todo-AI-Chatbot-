/**
 * Type Definitions for Todo Application
 * Defines all data models and API response types used throughout the application
 */

export enum TaskStatus {
  PENDING = 'pending',
  COMPLETED = 'completed',
  ARCHIVED = 'archived',
}

export enum TaskPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
}

export interface User {
  id: string
  email: string
  full_name: string
  avatar_url?: string
  created_at: string
  updated_at: string
}

export interface Task {
  id: string
  user_id: string
  title: string
  description?: string
  status: TaskStatus
  priority: TaskPriority
  due_date?: string
  created_at: string
  updated_at: string
  completed_at?: string
}

export interface TaskList {
  data: Task[]
  pagination: {
    page: number
    limit: number
    total: number
    pages: number
  }
}

export interface ApiError {
  detail?: string
  error_code?: string
  status?: number
  timestamp?: string
  message?: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
}

export interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: ApiError | null
  tokens: {
    accessToken: string | null
    refreshToken: string | null
  }
}

export interface TaskState {
  tasks: Task[]
  selectedTask: Task | null
  isLoading: boolean
  error: ApiError | null
  filters: {
    status?: TaskStatus
    priority?: TaskPriority
    search?: string
  }
  pagination: {
    page: number
    limit: number
    total: number
    pages: number
  }
}

export interface UIState {
  theme: 'light' | 'dark'
  sidebarOpen: boolean
  toasts: Toast[]
  modals: Record<string, boolean>
}

export interface Toast {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  message: string
  duration?: number
}

export interface CreateTaskInput {
  title: string
  description?: string
  priority?: TaskPriority
  due_date?: string
}

export interface UpdateTaskInput {
  title?: string
  description?: string
  status?: TaskStatus
  priority?: TaskPriority
  due_date?: string
  completed_at?: string
}

export interface UpdateUserInput {
  full_name?: string
  avatar_url?: string
}

export interface ChangePasswordInput {
  old_password: string
  new_password: string
}

export interface LoginInput {
  email: string
  password: string
}

export interface SignUpInput {
  email: string
  full_name: string
  password: string
}

export interface TaskFilterOptions {
  status?: TaskStatus
  priority?: TaskPriority
  sortBy?: 'due_date' | 'created_at' | 'priority'
  order?: 'asc' | 'desc'
  page?: number
  limit?: number
  search?: string
}

export interface PaginationParams {
  page: number
  limit: number
}

export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: ApiError
}
