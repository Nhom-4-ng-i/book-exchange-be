from app.services.supabase import get_supabase


def get_course_name_by_id(course_id: int):
    supabase = get_supabase()
    res = supabase.table("courses").select(
        "*").eq("course_id", course_id).single().execute()
    return res.data


def get_course_id_by_name(course_name: str):
    supabase = get_supabase()
    res = supabase.table("courses").select(
        "*").eq("course_name", course_name).single().execute()
    return res.data


def get_all_courses():
    supabase = get_supabase()
    res = supabase.table("courses").select("*").execute()
    return res.data
