/**
 * Loading Component
 * Loading spinner and skeleton loaders
 * Task: 02-077
 */

'use client'

import React from 'react'

interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

/**
 * Spinner component for loading states
 */
export function Spinner({ size = 'md', className = '' }: SpinnerProps) {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-6 w-6',
    lg: 'h-8 w-8',
  }

  return (
    <svg
      className={`${sizeClasses[size]} animate-spin text-current ${className}`}
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
  )
}

interface LoadingOverlayProps {
  isLoading: boolean
  children: React.ReactNode
}

/**
 * Full-screen loading overlay
 */
export function LoadingOverlay({ isLoading, children }: LoadingOverlayProps) {
  if (!isLoading) return <>{children}</>

  return (
    <div className="relative">
      {children}
      <div className="absolute inset-0 flex items-center justify-center rounded-lg bg-slate-950/80 backdrop-blur-sm">
        <Spinner size="lg" className="text-indigo-500" />
      </div>
    </div>
  )
}

interface SkeletonProps {
  count?: number
  height?: string
  circle?: boolean
  className?: string
}

/**
 * Skeleton loader for content placeholders
 */
export function Skeleton({
  count = 1,
  height = 'h-4',
  circle = false,
  className = '',
}: SkeletonProps) {
  return (
    <>
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className={`mb-3 animate-pulse ${height} ${
            circle ? 'rounded-full' : 'rounded'
          } bg-slate-800 ${className}`}
        />
      ))}
    </>
  )
}

interface ButtonLoadingProps {
  isLoading: boolean
  children: React.ReactNode
}

/**
 * Loading state for buttons
 */
export function ButtonLoading({ isLoading, children }: ButtonLoadingProps) {
  if (!isLoading) return <>{children}</>

  return (
    <div className="flex items-center gap-2">
      <Spinner size="sm" className="text-current" />
      <span>Loading...</span>
    </div>
  )
}

interface SkeletonCardProps {
  count?: number
}

/**
 * Skeleton card for task list placeholders
 */
export function SkeletonCard({ count = 3 }: SkeletonCardProps) {
  return (
    <>
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="mb-4 rounded-xl border border-slate-800 p-4 bg-slate-900/50"
        >
          <Skeleton height="h-6" className="mb-2" />
          <Skeleton height="h-4" count={2} />
          <div className="mt-4 flex gap-2">
            <Skeleton height="h-8" className="w-16 rounded-full" />
            <Skeleton height="h-8" className="w-16 rounded-full" />
          </div>
        </div>
      ))}
    </>
  )
}

/**
 * Full page loading state
 */
export function PageLoading() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[#020617]">
      <div className="text-center">
        <div className="relative mb-6">
           <Spinner size="lg" className="mx-auto text-indigo-500" />
           <div className="absolute inset-0 bg-indigo-500/20 blur-xl rounded-full"></div>
        </div>
        <p className="text-slate-400 font-bold tracking-widest animate-pulse uppercase text-xs">Synchronizing</p>
      </div>
    </div>
  )
}

export default {
  Spinner,
  LoadingOverlay,
  Skeleton,
  ButtonLoading,
  SkeletonCard,
  PageLoading,
}