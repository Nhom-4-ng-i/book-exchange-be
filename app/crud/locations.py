from app.services.supabase import get_supabase


def get_locations_list():
    supabase = get_supabase()
    response = (
        supabase
        .table("locations")
        .select("name", "id")
        .execute()
    )
    return response.data
