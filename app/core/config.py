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


@lru_cache()
def get_settings() -> Settings:
    return Settings()