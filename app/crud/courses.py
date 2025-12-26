from app.services.supabase import get_supabase


def get_courses_list():
    supabase = get_supabase()
    response = (
        supabase
        .table("courses")
        .select("*")
        .execute()
    )
    return response.data
