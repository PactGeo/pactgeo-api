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
    DATABASE_URI: str = "postgresql://postgres:dHeiAMxVgVPsWIPwELWiZSpPnFYvbAau@autorack.proxy.rlwy.net:58133/railway"
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

class TestSettings(Settings):
    class Config:
        case_sensitive = True

test_settings = TestSettings()
