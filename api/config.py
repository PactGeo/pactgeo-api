import os
import secrets
from typing import Literal
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = f"Geounity API - {os.getenv('ENV', 'development')}"
    DESCRIPTION: str = "API for Geounity project, using FastAPI and SQLModel"
    ENV: Literal["development", "staging", "production"] = "development"
    VERSION: str = "0.1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DATABASE_URI: str = "sqlite:///./geounity.db"
    API_USERNAME: str = "seba"
    API_PASSWORD: str = "123456"

    class Config:
        case_sensitive = True

settings = Settings()

class TestSettings(Settings):
    class Config:
        case_sensitive = True

test_settings = TestSettings()
