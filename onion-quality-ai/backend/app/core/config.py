"""
Application configuration loaded from environment variables.

Uses pydantic-settings so that every value can be overridden via .env or
OS-level environment variables without touching source code.
"""

from functools import lru_cache
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central, validated configuration for the backend."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # --- Application ---
    app_name: str = "onion-quality-backend"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = False

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, v: Any) -> bool:
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            val = v.strip().lower()
            if val in ("true", "1", "t", "yes", "y", "debug", "dev", "development"):
                return True
            if val in ("false", "0", "f", "no", "n", "release", "prod", "production"):
                return False
        return bool(v)

    # --- Database ---
    database_url: str = "postgresql+asyncpg://postgres:changeme@localhost:5432/onion_quality"

    # --- Directories ---
    model_directory: str = "./models"
    image_directory: str = "./data/raw"
    report_directory: str = "./reports"

    # --- Upload Limits ---
    max_image_size_mb: int = 10


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (created once per process)."""
    return Settings()
