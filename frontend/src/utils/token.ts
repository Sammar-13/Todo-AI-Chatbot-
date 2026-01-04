/**
 * Token Utility Functions
 * Helper functions for JWT token manipulation
 * Task: 40
 */

interface JWTPayload {
  sub?: string
  exp?: number
  iat?: number
  [key: string]: unknown
}

/**
 * Parse JWT token and extract payload
 */
export function parseJWT(token: string): JWTPayload {
  try {
    const parts = token.split('.')
    if (parts.length !== 3) {
      throw new Error('Invalid token format')
    }

    const payload = parts[1]
    const decoded = JSON.parse(atob(payload))
    return decoded
  } catch (error) {
    console.error('Error parsing JWT:', error)
    return {}
  }
}

/**
 * Check if token is expired
 */
export function isTokenExpired(token: string): boolean {
  try {
    const payload = parseJWT(token)

    if (!payload.exp) {
      return false
    }

    // Check if token expires within the next minute
    const now = Math.floor(Date.now() / 1000)
    return payload.exp < now + 60
  } catch {
    return true
  }
}

/**
 * Get token expiration time as Date
 */
export function getExpirationTime(token: string): Date | null {
  try {
    const payload = parseJWT(token)

    if (!payload.exp) {
      return null
    }

    return new Date(payload.exp * 1000)
  } catch {
    return null
  }
}

/**
 * Get time until token expiration in milliseconds
 */
export function getTimeUntilExpiration(token: string): number | null {
  try {
    const payload = parseJWT(token)

    if (!payload.exp) {
      return null
    }

    const expirationTime = payload.exp * 1000
    const now = Date.now()
    return expirationTime - now
  } catch {
    return null
  }
}

/**
 * Extract user ID from token
 */
export function getUserIdFromToken(token: string): string | null {
  try {
    const payload = parseJWT(token)
    return (payload.sub as string) || null
  } catch {
    return null
  }
}

export default {
  parseJWT,
  isTokenExpired,
  getExpirationTime,
  getTimeUntilExpiration,
  getUserIdFromToken,
}
