from app.services.supabase import get_supabase


def get_profile(user_id: str):
    supabase = get_supabase()
    return (
        supabase
        .table("profiles")
        .select("*")
        .eq("user_id", user_id)
        .single()
        .execute()
    ).data


def insert_profile(user_id: str, name: str, email: str):
    supabase = get_supabase()
    (
        supabase
        .table("profiles")
        .insert({
            "user_id": user_id,
            "name": name,
            "email": email
        })
        .execute()
    )


def update_profile(user_id: str, name: str = None, email: str = None):
    supabase = get_supabase()
    profile = {}
    if name is not None:
        profile["name"] = name
    if email is not None:
        profile["email"] = email
    supabase.table("profiles").update(profile).eq("user_id", user_id).execute()
