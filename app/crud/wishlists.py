from app.services.supabase import get_supabase


def insert_wishlist(user_id: str, title: str, course_id: int, max_price: int):
    supabase = get_supabase()
    supabase.table("wishlists").insert({
        "user_id": user_id,
        "title": title,
        "course_id": course_id,
        "max_price": max_price,
    }).execute()


def update_wishlist(user_id: str, wishlist_id: int, title: str, course_id: int, max_price: int):
    supabase = get_supabase()
    supabase.table("wishlists").update({
        "title": title,
        "course_id": course_id,
        "max_price": max_price,
    }).eq("id", wishlist_id).eq("user_id", user_id).execute()


def delete_wishlist(user_id: str, wishlist_id: int):
    supabase = get_supabase()
    supabase.table("wishlists").delete().eq(
        "id", wishlist_id).eq("user_id", user_id).execute()

def get_wishlists_by_user(user_id: str):
    supabase = get_supabase()
    # Lấy toàn bộ cột của wishlist theo user_id, sắp xếp mới nhất lên đầu
    response = supabase.table("wishlists")\
        .select("*")\
        .eq("user_id", user_id)\
        .order("created_at", desc=True)\
        .execute()
        
    return response.data