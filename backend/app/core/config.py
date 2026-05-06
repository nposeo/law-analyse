from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache
from typing import Union


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    database_url: str = ""
    openai_api_key: str = ""
    environment: str = "development"

    # CORS settings - can be string (comma-separated) or list
    cors_origins: Union[str, list[str]] = "http://localhost:4321,http://localhost:3000"

    # File upload settings
    max_upload_size: int = 50 * 1024 * 1024  # 50MB
    allowed_extensions: set[str] = {".pdf"}

    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
