from app.services.supabase import get_supabase


def get_all_courses():
    supabase = get_supabase()
    res = supabase.table("courses").select("*").execute()
    return res.data


def get_course_name_by_id(course_id: int):
    supabase = get_supabase()
    res = supabase.table("courses").select(
        "*").eq("id", course_id).single().execute()
    return res.data


def get_course_id_by_name(course_name: str):
    supabase = get_supabase()
    res = supabase.table("courses").select(
        "*").eq("name", course_name).single().execute()
    return res.data


def insert_course(name: str):
    supabase = get_supabase()
    supabase.table("courses").insert({
        "name": name
    }).execute()


def update_course_by_id(course_id: int, name: str):
    supabase = get_supabase()
    supabase.table("courses").update({
        "name": name
    }).eq("id", course_id).execute()


def update_course_by_name(course_name: str, name: str):
    supabase = get_supabase()
    supabase.table("courses").update({
        "name": name
    }).eq("name", course_name).execute()


def delete_course_by_id(course_id: int):
    supabase = get_supabase()
    supabase.table("courses").delete().eq("id", course_id).execute()


def delete_course_by_name(course_name: str):
    supabase = get_supabase()
    supabase.table("courses").delete().eq("name", course_name).execute()
