from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database settings
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    # Database URL
    DATABASE_URL: str

    # App metadata
    PROJECT_NAME: str = "URL Shortener"
    API_V1_STR: str = "/api/v1"  # <-- Add this

    # Other settings
    SECRET_KEY: str = "your_super_secret_key_change_this_in_production"
    BASE_URL: str = "http://localhost:8000"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    def get_database_url(self) -> str:
        return str(self.DATABASE_URL)

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"


settings = Settings()
