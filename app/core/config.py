from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_PASSWORD: str
    CLOUDINARY_URL: str
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str


@lru_cache()
def get_settings() -> Settings:
    return Settings()