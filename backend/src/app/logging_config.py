"""Logging configuration for the FastAPI application."""

import logging
import sys
from typing import Any, Dict

from .config import settings


def get_logger_config() -> Dict[str, Any]:
    """Get logging configuration dictionary.

    Returns:
        Dictionary with logging configuration
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
            },
        },
        "loggers": {
            "fastapi": {
                "handlers": ["default"],
                "level": log_level,
            },
            "sqlalchemy.engine": {
                "handlers": ["default"],
                "level": logging.WARNING,  # Suppress SQL query logging in production
            },
            "app": {
                "handlers": ["default"],
                "level": log_level,
            },
        },
    }


# Create module-level logger
logger = logging.getLogger("app")
