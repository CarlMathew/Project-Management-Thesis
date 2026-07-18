from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Project Management System API"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = False


    api_v1_prefix: str = "/api/v1"
    frontend_url: str = "http://localhost:5173"

    database_url: str = Field(
        default="",
        description="SQLAlchemy SQL Server connection string"
    )

    jwt_secret_key: str = Field(
        default="",
        description="Secret key used to sign JWTs"
    )

    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expired_days: int = 7

    model_config = SettingsConfigDict(
        env_file=".env"
    )


@lru_cache
def get_settings() -> Settings:
    """Setup Enviroment Information and Config for the app"""
    return Settings()


settings = get_settings()