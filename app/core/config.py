from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional, List
from pydantic import field_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_PASSWORD: str
    # Cloudinary configuration (optional)
    CLOUDINARY_URL: Optional[str] = None
    CLOUDINARY_CLOUD_NAME: Optional[str] = None
    CLOUDINARY_API_KEY: Optional[str] = None
    CLOUDINARY_API_SECRET: Optional[str] = None
    # CORS configuration (default: allow all)
    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = False
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @field_validator("CORS_METHODS", mode="before")
    @classmethod
    def parse_cors_methods(cls, v):
        if isinstance(v, str):
            return [method.strip() for method in v.split(",")]
        return v

    @field_validator("CORS_HEADERS", mode="before")
    @classmethod
    def parse_cors_headers(cls, v):
        if isinstance(v, str):
            return [header.strip() for header in v.split(",")]
        return v


@lru_cache()
def get_settings() -> Settings:
    return Settings()
