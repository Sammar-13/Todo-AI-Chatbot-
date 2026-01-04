/**
 * Users Service
 * Handles user profile and account management
 * Task: 02-058
 */

import apiClient from '@/utils/api'
import { User, UpdateUserInput, ChangePasswordInput } from '@/types'

class UsersService {
  /**
   * Get user profile
   */
  async getProfile(): Promise<User> {
    const response = await apiClient.fetchAPI<{ data: User }>(
      '/users/me',
      {
        method: 'GET',
      }
    )

    return response.data
  }

  /**
   * Update user profile
   */
  async updateProfile(data: UpdateUserInput): Promise<User> {
    const response = await apiClient.fetchAPI<{ data: User }>(
      '/users/me',
      {
        method: 'PUT',
        body: JSON.stringify(data),
      }
    )

    return response.data
  }

  /**
   * Change user password
   */
  async changePassword(data: ChangePasswordInput): Promise<void> {
    await apiClient.fetchAPI('/users/me/password', {
      method: 'PUT',
      body: JSON.stringify({
        old_password: data.old_password,
        new_password: data.new_password,
      }),
    })
  }

  /**
   * Get user by ID (admin or self)
   */
  async getUserById(userId: string): Promise<User> {
    const response = await apiClient.fetchAPI<{ data: User }>(
      `/users/${userId}`,
      {
        method: 'GET',
      }
    )

    return response.data
  }

  /**
   * Delete user account
   */
  async deleteAccount(): Promise<void> {
    await apiClient.fetchAPI('/users/me', {
      method: 'DELETE',
    })
  }
}

export const usersService = new UsersService()

export default usersService
