"""Application configuration using Pydantic settings (Task 02-024)."""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # =======================
    # Database
    # =======================
    DATABASE_URL: str = ""

    # Gemini
    @property
    def gemini_api_key(self) -> str:
        import os
        return os.getenv("GEMINI_API_KEY", self.GEMINI_API_KEY)

    GEMINI_API_KEY: str = "" 
    # ... remaining fields ...
    JWT_SECRET_KEY: str = "dev-secret-key-must-be-at-least-32-characters-long"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # =======================
    # Security
    # =======================
    BCRYPT_ROUNDS: int = 10

    # =======================
    # CORS (VERY IMPORTANT)
    # =======================
    CORS_ORIGINS: str = "http://localhost:3000,https://todo-ai-chatbot-frontend-fxdzkdc51.vercel.app,https://sammar20-todo-backend-iii.hf.space"
    """Comma-separated list of allowed origins."""

    # =======================
    # Application
    # =======================
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    LOG_LEVEL: str = "INFO"

    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000

    def __init__(self, **data):
        super().__init__(**data)
        if self.DATABASE_URL:
            self._validate_settings()

    def _validate_settings(self) -> None:
        if not self.DATABASE_URL.startswith(("postgresql", "sqlite")):
            raise ValueError(
                "Invalid DATABASE_URL. Must start with postgresql or sqlite"
            )

        if len(self.JWT_SECRET_KEY) < 32:
            raise ValueError("JWT_SECRET_KEY must be at least 32 characters")

        if not self.CORS_ORIGINS:
            raise ValueError("CORS_ORIGINS is required")

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"


settings = Settings()
