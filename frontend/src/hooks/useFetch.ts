/**
 * useFetch Hook
 * Generic hook for fetching data with loading, error, and refetch states
 * Task: 02-064
 */

'use client'

import { useEffect, useState, useCallback, useRef } from 'react'
import apiClient from '@/utils/api'
import { ApiError } from '@/types'

interface UseFetchOptions {
  skip?: boolean
  dependencies?: unknown[]
  onSuccess?: (data: unknown) => void
  onError?: (error: ApiError | Error) => void
}

interface UseFetchResult<T> {
  data: T | null
  isLoading: boolean
  error: ApiError | Error | null
  refetch: () => Promise<void>
}

export function useFetch<T = unknown>(
  url: string,
  options: UseFetchOptions = {}
): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null)
  const [isLoading, setIsLoading] = useState(!options.skip)
  const [error, setError] = useState<ApiError | Error | null>(null)
  const { skip = false, dependencies = [], onSuccess, onError } = options
  const abortControllerRef = useRef<AbortController | null>(null)

  const fetchData = useCallback(async () => {
    if (skip) {
      setIsLoading(false)
      return
    }

    // Cancel previous request if any
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }

    abortControllerRef.current = new AbortController()
    setIsLoading(true)
    setError(null)

    try {
      const result = await apiClient.fetchAPI<T>(url, {
        signal: abortControllerRef.current.signal,
      })

      setData(result)
      setError(null)
      onSuccess?.(result)
    } catch (err) {
      if (err instanceof Error && err.name !== 'AbortError') {
        setError(err)
        onError?.(err)
      }
    } finally {
      setIsLoading(false)
    }
  }, [url, skip, onSuccess, onError])

  // Initial fetch on mount
  useEffect(() => {
    fetchData()

    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
    }
  }, [fetchData, ...dependencies])

  const refetch = useCallback(async () => {
    await fetchData()
  }, [fetchData])

  return { data, isLoading, error, refetch }
}

export default useFetch
