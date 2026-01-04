"""Rate limiting middleware for FastAPI application."""

import time
from collections import defaultdict
from typing import Dict, Tuple

from fastapi import Request, status
from fastapi.responses import JSONResponse


class RateLimiter:
    """Simple in-memory rate limiter."""

    def __init__(self, requests_per_minute: int = 60):
        """Initialize rate limiter.

        Args:
            requests_per_minute: Max requests allowed per minute per IP
        """
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, client_ip: str) -> Tuple[bool, Dict]:
        """Check if request is allowed.

        Args:
            client_ip: Client IP address

        Returns:
            Tuple of (allowed: bool, headers: dict with rate limit info)
        """
        now = time.time()
        minute_ago = now - 60

        # Remove old requests outside the 1-minute window
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > minute_ago
        ]

        # Get current count
        current_count = len(self.requests[client_ip])
        allowed = current_count < self.requests_per_minute

        # Add current request if allowed
        if allowed:
            self.requests[client_ip].append(now)

        # Return headers for rate limit info
        headers = {
            "X-RateLimit-Limit": str(self.requests_per_minute),
            "X-RateLimit-Remaining": str(max(0, self.requests_per_minute - current_count - 1)),
            "X-RateLimit-Reset": str(int(now) + 60),
        }

        return allowed, headers


# Global rate limiter instance
rate_limiter = RateLimiter(requests_per_minute=100)


async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware.

    Limits requests to 100 per minute per IP address.
    Excludes health check and documentation endpoints.
    """
    # Skip rate limiting for health checks and docs
    if request.url.path in ("/health", "/api/health", "/docs", "/redoc", "/openapi.json"):
        return await call_next(request)

    # Get client IP
    client_ip = request.client.host if request.client else "unknown"

    # Check rate limit
    allowed, headers = rate_limiter.is_allowed(client_ip)

    if not allowed:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Rate limit exceeded. Max 100 requests per minute."},
            headers=headers,
        )

    # Process request
    response = await call_next(request)

    # Add rate limit headers to response
    for key, value in headers.items():
        response.headers[key] = value

    return response
