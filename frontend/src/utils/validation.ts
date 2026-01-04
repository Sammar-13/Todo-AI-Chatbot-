/**
 * Validation Utility Functions
 * Helper functions for form and data validation
 * Task: 42
 */

import { z } from 'zod'

/**
 * Validate email address format
 */
export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * Validate password strength
 * Returns object with validation result and specific errors
 */
export function validatePassword(password: string): {
  valid: boolean
  errors: string[]
} {
  const errors: string[] = []

  if (password.length < 8) {
    errors.push('Password must be at least 8 characters long')
  }

  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain at least one uppercase letter')
  }

  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain at least one lowercase letter')
  }

  if (!/[0-9]/.test(password)) {
    errors.push('Password must contain at least one number')
  }

  if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
    errors.push('Password must contain at least one special character')
  }

  return {
    valid: errors.length === 0,
    errors,
  }
}

/**
 * Validate task title
 */
export function validateTitle(title: string): boolean {
  if (!title) return false
  if (title.length < 3) return false
  if (title.length > 255) return false
  return true
}

/**
 * Validate task description
 */
export function validateDescription(description: string): boolean {
  if (!description) return true // Description is optional
  return description.length <= 5000
}

/**
 * Validate URL format
 */
export function validateUrl(url: string): boolean {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

/**
 * Validate name (full name)
 */
export function validateFullName(name: string): boolean {
  if (!name) return false
  if (name.length < 2) return false
  if (name.length > 255) return false
  return true
}

/**
 * Validate date format (ISO 8601)
 */
export function validateDate(dateString: string): boolean {
  try {
    const date = new Date(dateString)
    return date instanceof Date && !isNaN(date.getTime())
  } catch {
    return false
  }
}

/**
 * Check if date is in the future
 */
export function isFutureDate(dateString: string): boolean {
  if (!validateDate(dateString)) return false
  return new Date(dateString) > new Date()
}

/**
 * Zod schemas for form validation
 */

export const loginSchema = z.object({
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Invalid email address'),
  password: z
    .string()
    .min(1, 'Password is required')
    .min(8, 'Password must be at least 8 characters'),
})

export const signupSchema = z
  .object({
    email: z
      .string()
      .min(1, 'Email is required')
      .email('Invalid email address'),
    full_name: z
      .string()
      .min(2, 'Name must be at least 2 characters')
      .max(255, 'Name must be less than 255 characters'),
    password: z
      .string()
      .min(8, 'Password must be at least 8 characters')
      .regex(/[A-Z]/, 'Password must contain an uppercase letter')
      .regex(/[a-z]/, 'Password must contain a lowercase letter')
      .regex(/[0-9]/, 'Password must contain a number')
      .regex(
        /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/,
        'Password must contain a special character'
      ),
    password_confirm: z.string().min(1, 'Please confirm your password'),
  })
  .refine((data) => data.password === data.password_confirm, {
    message: 'Passwords do not match',
    path: ['password_confirm'],
  })

export const createTaskSchema = z.object({
  title: z
    .string()
    .min(3, 'Title must be at least 3 characters')
    .max(255, 'Title must be less than 255 characters'),
  description: z
    .string()
    .max(5000, 'Description must be less than 5000 characters')
    .optional(),
  priority: z
    .enum(['low', 'medium', 'high'])
    .default('medium'),
  due_date: z
    .string()
    .datetime()
    .optional(),
})

export const updateTaskSchema = z.object({
  title: z
    .string()
    .min(3, 'Title must be at least 3 characters')
    .max(255, 'Title must be less than 255 characters')
    .optional(),
  description: z
    .string()
    .max(5000, 'Description must be less than 5000 characters')
    .optional(),
  status: z
    .enum(['pending', 'completed', 'archived'])
    .optional(),
  priority: z
    .enum(['low', 'medium', 'high'])
    .optional(),
  due_date: z
    .string()
    .datetime()
    .optional(),
})

export const updateProfileSchema = z.object({
  full_name: z
    .string()
    .min(2, 'Name must be at least 2 characters')
    .max(255, 'Name must be less than 255 characters')
    .optional(),
  avatar_url: z
    .string()
    .url('Invalid URL')
    .optional(),
})

export const changePasswordSchema = z
  .object({
    old_password: z
      .string()
      .min(1, 'Current password is required'),
    new_password: z
      .string()
      .min(8, 'Password must be at least 8 characters')
      .regex(/[A-Z]/, 'Password must contain an uppercase letter')
      .regex(/[a-z]/, 'Password must contain a lowercase letter')
      .regex(/[0-9]/, 'Password must contain a number')
      .regex(
        /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/,
        'Password must contain a special character'
      ),
    confirm_password: z.string().min(1, 'Please confirm your password'),
  })
  .refine((data) => data.new_password === data.confirm_password, {
    message: 'Passwords do not match',
    path: ['confirm_password'],
  })

export default {
  validateEmail,
  validatePassword,
  validateTitle,
  validateDescription,
  validateUrl,
  validateFullName,
  validateDate,
  isFutureDate,
  loginSchema,
  signupSchema,
  createTaskSchema,
  updateTaskSchema,
  updateProfileSchema,
  changePasswordSchema,
}
