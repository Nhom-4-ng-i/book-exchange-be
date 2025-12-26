from app.services.supabase import get_supabase
from typing import Optional


def _base_wishlists_query(supabase):
    return (
        supabase
        .table("wishlists")
        .select(
            "*"
        )
    )


def get_wishlists_list(user_id: Optional[str] = None, book_title: Optional[str] = None, course_id: Optional[int] = None, max_price: Optional[int] = None, seller_id: Optional[str] = None):
    supabase = get_supabase()

    query = _base_wishlists_query(supabase)

    if user_id is not None:
        query = query.eq("user_id", user_id)

    if course_id is not None:
        query = query.or_(f"course_id.is.null,course_id.eq.{course_id}")

    if max_price is not None:
        query = query.or_(f"max_price.is.null,max_price.gte.{max_price}")

    if seller_id is not None:
        query = query.neq("user_id", seller_id)

    if book_title is not None:
        query = query.text_search("title", f"'{book_title}'")

    return query.execute().data


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
