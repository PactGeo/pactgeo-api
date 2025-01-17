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
    API_USERNAME: str = "seba"
    API_PASSWORD: str = "123456"
    AUTH_SECRET: str = "zEV3nYEGdn/WmgqJihRfb4hcJ9NdhO8ESeUqoWgN0TU="
    JWT_SECRET: str = "1234567890"
    DATABASE_URI: str = "postgresql://seba:123456@localhost/geounity_db"
    CLOUDINARY_CLOUD_NAME: str = "geounity"
    CLOUDINARY_API_KEY: str = "813557857562179"
    CLOUDINARY_API_SECRET: str = "cWtbOjvAtiyTk7CJh5Zw6lKZCkQ"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()

class TestSettings(Settings):
    class Config:
        case_sensitive = True

test_settings = TestSettings()
