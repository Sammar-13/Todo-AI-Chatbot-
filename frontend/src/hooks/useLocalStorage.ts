/**
 * useLocalStorage Hook
 * Type-safe hook for localStorage with sync across tabs
 * Task: 02-065
 */

'use client'

import { useState, useEffect, useCallback } from 'react'

interface UseLocalStorageResult<T> {
  value: T
  setValue: (value: T | ((prev: T) => T)) => void
  removeValue: () => void
  isLoading: boolean
}

export function useLocalStorage<T = unknown>(
  key: string,
  initialValue?: T
): UseLocalStorageResult<T> {
  const [value, setValue] = useState<T>(initialValue as T)
  const [isLoading, setIsLoading] = useState(true)

  // Initialize value from localStorage
  useEffect(() => {
    try {
      if (typeof window === 'undefined') {
        return
      }

      const stored = localStorage.getItem(key)
      if (stored !== null) {
        try {
          setValue(JSON.parse(stored))
        } catch {
          // If parse fails, use the string value
          setValue(stored as unknown as T)
        }
      } else if (initialValue !== undefined) {
        setValue(initialValue)
      }
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error)
    } finally {
      setIsLoading(false)
    }
  }, [key, initialValue])

  // Persist to localStorage when value changes
  const handleSetValue = useCallback((newValue: T | ((prev: T) => T)) => {
    try {
      if (typeof window === 'undefined') {
        return
      }

      setValue((prev) => {
        const actualValue =
          typeof newValue === 'function'
            ? (newValue as (prev: T) => T)(prev)
            : newValue

        if (actualValue === undefined) {
          localStorage.removeItem(key)
        } else {
          localStorage.setItem(key, JSON.stringify(actualValue))
        }

        return actualValue
      })
    } catch (error) {
      console.error(`Error writing to localStorage key "${key}":`, error)
    }
  }, [key])

  // Remove value from localStorage
  const removeValue = useCallback(() => {
    try {
      if (typeof window === 'undefined') {
        return
      }

      localStorage.removeItem(key)
      setValue(initialValue as T)
    } catch (error) {
      console.error(`Error removing localStorage key "${key}":`, error)
    }
  }, [key, initialValue])

  // Listen for changes from other tabs
  useEffect(() => {
    if (typeof window === 'undefined') {
      return
    }

    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === key && e.newValue !== null) {
        try {
          setValue(JSON.parse(e.newValue))
        } catch {
          setValue(e.newValue as unknown as T)
        }
      }
    }

    window.addEventListener('storage', handleStorageChange)
    return () => {
      window.removeEventListener('storage', handleStorageChange)
    }
  }, [key])

  return {
    value,
    setValue: handleSetValue,
    removeValue,
    isLoading,
  }
}

export default useLocalStorage
