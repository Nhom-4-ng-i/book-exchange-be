from app.services.supabase import get_supabase


def get_locations_list():
    supabase = get_supabase()
    res = supabase.table("locations").select(
        "*").execute()
    return res.data


def get_location(id: int):
    supabase = get_supabase()
    res = supabase.table("locations").select(
        "*").eq("id", id).single().execute()
    return res.data


def insert_location(name: str):
    supabase = get_supabase()
    supabase.table("locations").insert({
        "name": name
    }).execute()


def update_location(id: int, name: str):
    supabase = get_supabase()
    supabase.table("locations").update({
        "name": name
    }).eq("id", id).execute()


def delete_location(id: int):
    supabase = get_supabase()
    supabase.table("locations").delete().eq("id", id).execute()
