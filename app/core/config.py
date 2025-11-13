from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional

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


@lru_cache()
def get_settings() -> Settings:
    return Settings()