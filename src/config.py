from __future__ import annotations

import os
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings

# Load .env if present
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Bỏ qua các biến môi trường không khai báo
        case_sensitive=False,
    )

    # ========== Database ==========
    DATABASE_URL: str = Field(
        default="sqlite:///./sen_v3.db",
        description="Database connection URL"
    )

    # ========== JWT Authentication ==========
    JWT_SECRET_KEY: str = Field(
        default="your-super-secret-key-change-in-production-min-32-chars",
        min_length=32,
        description="Secret key for JWT signing (min 32 chars)"
    )
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT signing algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Access token expiry in minutes")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, description="Refresh token expiry in days")

    # ========== Encryption ==========
    ENCRYPTION_KEY: Optional[str] = Field(
        default=None,
        description="Fernet encryption key for sensitive data"
    )

    # ========== CORS ==========
    CORS_ORIGINS: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        description="Comma-separated list of allowed CORS origins"
    )

    # ========== External APIs ==========
    GEMINI_API_KEY: Optional[str] = Field(default=None, description="Google Gemini API key")
    GROQ_API_KEY: Optional[str] = Field(default=None, description="Groq API key")
    ACCESS_TRADE_ACCESS_KEY: Optional[str] = Field(default=None, description="AccessTrade API key")
    ACCESS_TRADE_API_SECRET: Optional[str] = Field(default=None, description="AccessTrade API secret")

    # ========== Logging ==========
    LOG_LEVEL: str = Field(default="INFO", description="Logging level (DEBUG, INFO, WARNING, ERROR)")

    # ========== Worker Settings ==========
    WORKER_POLL_INTERVAL_SECONDS: int = Field(default=2, description="Worker polling interval in seconds")
    MAX_CONCURRENT_WORKERS: int = Field(default=5, description="Maximum number of concurrent workers")

    # ========== PostgreSQL (optional) ==========
    POSTGRES_USER: Optional[str] = Field(default=None, description="PostgreSQL username")
    POSTGRES_PASSWORD: Optional[str] = Field(default=None, description="PostgreSQL password")
    POSTGRES_DB: Optional[str] = Field(default=None, description="PostgreSQL database name")
    POSTGRES_HOST: Optional[str] = Field(default="localhost", description="PostgreSQL host")
    POSTGRES_PORT: int = Field(default=5432, description="PostgreSQL port")

    # ========== MinIO (optional) ==========
    MINIO_ROOT_USER: Optional[str] = Field(default=None, description="MinIO root username")
    MINIO_ROOT_PASSWORD: Optional[str] = Field(default=None, description="MinIO root password")

    # ========== Helper Properties ==========
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS_ORIGINS string into a list."""
        if not self.CORS_ORIGINS:
            return []
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def is_postgres_configured(self) -> bool:
        """Check if PostgreSQL is fully configured."""
        return all([
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_DB,
        ])

    @property
    def postgres_url(self) -> Optional[str]:
        """Build PostgreSQL connection URL if configured."""
        if not self.is_postgres_configured:
            return None
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


# Create global settings instance
settings = Settings()

# Validate critical settings on startup
if settings.JWT_SECRET_KEY == "your-super-secret-key-change-in-production-min-32-chars":
    import warnings
    warnings.warn(
        "⚠️ JWT_SECRET_KEY is using default value! Please change it in .env file for production!",
        UserWarning
    )

if len(settings.JWT_SECRET_KEY) < 32:
    import warnings
    warnings.warn(
        f"⚠️ JWT_SECRET_KEY length is {len(settings.JWT_SECRET_KEY)} chars. "
        "Recommended minimum is 32 chars for security!",
        UserWarning
    )