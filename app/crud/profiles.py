from app.services.supabase import get_supabase


def create_profile(user_id: str, name: str, email: str):
    supabase = get_supabase()
    supabase.table("profiles").insert({
        "user_id": user_id,
        "name": name,
        "email": email
    }).execute()
    
def get_profile(user_id: str):
    supabase = get_supabase()
    return supabase.table("profiles").select("*").eq("user_id", user_id).single().execute()