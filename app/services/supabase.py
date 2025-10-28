from supabase import create_client, Client
from functools import lru_cache
from app.core.config import get_settings

settings = get_settings()

@lru_cache()
def get_supabase() -> Client:
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
