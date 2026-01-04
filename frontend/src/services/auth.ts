/**
 * Authentication Service
 * Handles user authentication operations
 * Task: 02-056
 */

import apiClient from '@/utils/api'
import { TokenResponse, User, LoginInput, SignUpInput } from '@/types'

class AuthService {
  /**
   * Register a new user account
   */
  async signup(data: SignUpInput): Promise<TokenResponse> {
    const response = await apiClient.fetchAPI<TokenResponse>(
      '/auth/register',
      {
        method: 'POST',
        body: JSON.stringify({
          email: data.email,
          password: data.password,
          full_name: data.full_name,
        }),
        skipAuth: true,
        skipRefresh: true,
      }
    )
    return response
  }

  /**
   * Login with email and password
   */
  async login(data: LoginInput): Promise<TokenResponse> {
    const response = await apiClient.fetchAPI<TokenResponse>(
      '/auth/login',
      {
        method: 'POST',
        body: JSON.stringify({
          email: data.email,
          password: data.password,
        }),
        skipAuth: true,
        skipRefresh: true,
      }
    )
    return response
  }

  /**
   * Refresh access token using refresh token
   */
  async refresh(): Promise<TokenResponse> {
    return apiClient.refreshAccessToken()
  }

  /**
   * Logout user (clear tokens on client)
   */
  async logout(): Promise<void> {
    try {
      await apiClient.fetchAPI('/auth/logout', {
        method: 'POST',
      })
    } finally {
      apiClient.logout()
    }
  }

  /**
   * Verify current session using cookies
   */
  async verifySession(): Promise<{ authenticated: boolean; user: User | null }> {
    try {
      const response = await apiClient.fetchAPI<{ authenticated: boolean; user: User | null }>(
        '/auth/verify',
        {
          method: 'GET',
          skipRefresh: true, // Don't try to refresh if verify fails
        }
      )
      return response
    } catch (error) {
      return { authenticated: false, user: null }
    }
  }

  /**
   * Get current authenticated user
   */
  async getCurrentUser(): Promise<User> {
    const response = await apiClient.fetchAPI<{ data: User }>(
      '/users/me',
      {
        method: 'GET',
      }
    )
    return response.data
  }
}

export const authService = new AuthService()

export default authService
