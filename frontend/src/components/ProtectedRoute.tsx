/**
 * Protected Route Component
 * Wraps pages to enforce authentication requirements
 * Task: 02-050
 */

'use client'

import { ReactNode, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import { PageLoading } from '@/components/Common/Loading'

interface ProtectedRouteProps {
  children: ReactNode
  requireAuth?: boolean
}

/**
 * ProtectedRoute Component
 *
 * Protects routes based on authentication status:
 * - requireAuth={true}: User must be logged in to view (redirects to /login)
 * - requireAuth={false}: User must be logged out to view (redirects to /tasks)
 *
 * @param children - Content to render if access is allowed
 * @param requireAuth - If true, requires authentication. If false, requires no authentication
 */
export function ProtectedRoute({
  children,
  requireAuth = true,
}: ProtectedRouteProps): ReactNode {
  const { isAuthenticated, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    // Don't do anything while loading
    if (isLoading) return

    // Check if user should have access to this route
    if (requireAuth && !isAuthenticated) {
      // User must be logged in but isn't
      router.push('/login')
    } else if (!requireAuth && isAuthenticated) {
      // User must be logged out but is logged in
      router.push('/tasks')
    }
  }, [isAuthenticated, isLoading, requireAuth, router])

  // Show loading spinner while checking authentication
  if (isLoading) {
    return <PageLoading />
  }

  // If requiring auth and not authenticated, don't render (will redirect)
  if (requireAuth && !isAuthenticated) {
    return null
  }

  // If requiring no auth and is authenticated, don't render (will redirect)
  if (!requireAuth && isAuthenticated) {
    return null
  }

  // User has access, render children
  return <>{children}</>
}

export default ProtectedRoute
