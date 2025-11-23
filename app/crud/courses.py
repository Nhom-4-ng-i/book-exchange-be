from app.services.supabase import get_supabase


def get_courses_list():
    supabase = get_supabase()
    res = supabase.table("courses").select(
        "*").execute()
    return res.data


def get_course(id: int):
    supabase = get_supabase()
    res = supabase.table("courses").select(
        "*").eq("id", id).single().execute()
    return res.data


def insert_course(name: str):
    supabase = get_supabase()
    supabase.table("courses").insert({
        "name": name
    }).execute()


def update_course(id: int, name: str):
    supabase = get_supabase()
    supabase.table("courses").update({
        "name": name
    }).eq("id", id).execute()


def delete_course(id: int):
    supabase = get_supabase()
    supabase.table("courses").delete().eq("id", id).execute()
