"""Vercel serverless entry point for FastAPI application.

IMPORTANT: This file is the ONLY entry point for Vercel's serverless functions.
Everything MUST be importable without errors.

How Vercel calls this:
1. Vercel imports this file during deployment
2. Looks for an `app` variable that is an ASGI application
3. Calls app(scope, receive, send) for each HTTP request

Common issues that cause FUNCTION_INVOCATION_FAILED:
- Importing modules that raise exceptions
- Trying to validate config at import time
- Creating database connections at import time
- Missing environment variables

Fix: Keep this file minimal and only import the FastAPI app.
"""

import sys
import logging
from pathlib import Path

# Configure basic logging FIRST to catch any errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vercel_handler")

try:
    # Add parent directory to path (backend/)
    backend_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(backend_dir))
    logger.info("Python path configured")

    # Import the FastAPI app
    # This MUST NOT raise any exceptions
    from src.app.main import app
    logger.info("FastAPI app imported successfully")

    # If we get here, the app is ready
    logger.info("Vercel serverless handler ready")

except Exception as e:
    # Log the full error for debugging
    logger.exception(f"FATAL: Failed to import FastAPI app: {e}")

    # Provide a fallback ASGI app that returns error details
    # This prevents "FUNCTION_INVOCATION_FAILED" with no error message
    async def error_app(scope, receive, send):
        """Fallback error handler for import failures."""
        if scope["type"] != "http":
            await send({"type": "http.disconnect"})
            return

        # Send error response
        import json
        error_content = json.dumps({
            "error": "FUNCTION_INVOCATION_FAILED",
            "detail": str(e),
            "type": type(e).__name__
        }).encode("utf-8")

        await send(
            {
                "type": "http.response.start",
                "status": 500,
                "headers": [[b"content-type", b"application/json"]],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": error_content,
            }
        )

    app = error_app
    # Do not raise the exception, otherwise Vercel will report a crash
    # and not use our fallback app.


