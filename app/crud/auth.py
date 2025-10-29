from app.services.supabase import get_supabase


def supabase_sign_up(email: str, password: str = "password"):
    supabase = get_supabase()
    return supabase.auth.sign_up(
        {
            "email": email,
            "password": password
        }
    )
    
def supabase_sign_in(email: str, password: str = "password"):
    supabase = get_supabase()
    return supabase.auth.sign_in_with_password(
        {
            "email": email,
            "password": password
        }
    )