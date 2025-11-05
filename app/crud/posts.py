from typing import Optional, List, Any
from app.services.supabase import get_supabase
from app.schemas.posts import Status, Course, BookStatus, Location
from app.services.cloudinary_client import upload_image_to_cloudinary


def get_post_by_id(post_id: int):
    supabase = get_supabase()
    return (
        supabase
        .table("posts")
        .select("*")
        .eq("post_id", post_id)
        .single()
        .execute()
    ).data


def insert_post(book_title: str, author: str, course: Course, book_status: BookStatus, price: int, location: Location, location_detail: Optional[str] = None, original_price: Optional[int] = None, description: Optional[str] = None, avatar: Optional[Any] = None, user_id: Optional[str] = None):
    supabase = get_supabase()

    avatar_url = None
    if avatar:
        if isinstance(avatar, str) and (avatar.startswith('http://') or avatar.startswith('https://')):
            avatar_url = avatar
        else:
            try:
                avatar_url = upload_image_to_cloudinary(avatar)
            except Exception:
                avatar_url = None

    payload = {
        "book_title": book_title,
        "author": author,
        "course": course,
        "book_status": book_status,
        "price": price,
        "original_price": original_price,
        "description": description,
        "location": location,
        "location_detail": location_detail,
    }
    if user_id:
        payload['user_id'] = user_id
    if avatar_url:
        payload['avatar'] = avatar_url

    supabase.table("posts").insert(payload).execute()


def search_posts(status: List[Status], book_title: Optional[str] = None, author: Optional[str] = None, course: Optional[Course] = None, book_status: Optional[BookStatus] = None, location: Optional[Location] = None, min_price: Optional[int] = None, max_price: Optional[int] = None):
    supabase = get_supabase()

    # Search with filters
    if book_title:
        response = (
            supabase.table("posts")
            .select("*")
            .in_("status", [status.value for status in status])
            .text_search("book_title", f"'{book_title}'")
            .execute()
        ).data

        if author:
            response = [x for x in response if x["author"] == author]
        if course:
            response = [x for x in response if x["course"] == course]
        if book_status:
            response = [x for x in response if x["book_status"] == book_status]
        if location:
            response = [x for x in response if x["location"] == location]
        if min_price:
            response = [x for x in response if x["price"] >= min_price]
        if max_price:
            response = [x for x in response if x["price"] <= max_price]
        return response

    # Search all posts with
    else:
        response = (
            supabase.table("posts")
            .select("*")
            .in_("status", [status.value for status in status])
            .execute()
        ).data
        return response
