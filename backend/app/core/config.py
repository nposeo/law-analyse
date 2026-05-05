from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    database_url: str
    openai_api_key: str
    environment: str = "development"

    # CORS settings
    cors_origins: list[str] = ["http://localhost:4321", "http://localhost:3000"]

    # File upload settings
    max_upload_size: int = 50 * 1024 * 1024  # 50MB
    allowed_extensions: set[str] = {".pdf"}

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
