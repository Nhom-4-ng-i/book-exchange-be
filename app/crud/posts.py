from typing import Optional, List
from app.services.supabase import get_supabase
from app.services.cloudinary_client import upload_image_to_cloudinary


def get_posts_list(
    status: Optional[List[str]] = None,
    book_title: Optional[str] = None,
    author: Optional[str] = None,
    book_status: Optional[str] = None,
    course_id: Optional[int] = None,
    location_id: Optional[int] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    seller_id: Optional[str] = None,
):
    supabase = get_supabase()

    query = (
        supabase
        .table("posts")
        .select(
            """
            *,
            courses(name),
            locations(name),
            book_status(code, name),
            post_status(code, name),
            profiles(name)
            """
        )
    )

    if status is not None:
        query = query.in_("post_status.code", status)

    if book_title is not None:
        query = query.text_search("book_title", f"'{book_title}'")

    if author is not None:
        query = query.eq("author", author)

    if book_status is not None:
        query = query.eq("book_status.code", book_status)

    if course_id is not None:
        query = query.eq("course_id", course_id)

    if location_id is not None:
        query = query.eq("location_id", location_id)

    if min_price is not None:
        query = query.gte("price", min_price)

    if max_price is not None:
        query = query.lte("price", max_price)

    if seller_id is not None:
        query = query.eq("user_id", seller_id)

    response = query.execute()
    raw_posts = response.data or []

    normalized_posts = []
    for row in raw_posts:
        normalized_posts.append({
            "id": row["id"],
            "book_title": row["book_title"],
            "author": row["author"],
            "price": row["price"],
            "created_at": row["created_at"],
            "avatar_url": row["avatar_url"],
            "course": row.get("courses", {}).get("name"),
            "location": row.get("locations", {}).get("name"),
            "book_status": row.get("book_status", {}).get("name"),
            "status": row.get("post_status", {}).get("name"),
            "seller_name": row.get("profiles", {}).get("name"),
        })

    return normalized_posts


def get_post(id: int):
    supabase = get_supabase()
    query = (
        supabase
        .table("posts")
        .select("*")
        .eq("id", id)
        .single()
    )
    response = query.execute()
    return response.data


def insert_post(
    user_id: str,
    status: str,
    book_title: str,
    author: str,
    course_id: int,
    book_status: str,
    price: int,
    location_id: int,
    location_detail: Optional[str],
    original_price: Optional[int],
    description: Optional[str],
):
    supabase = get_supabase()

    post = {
        "book_title": book_title,
        "status": status,
        "author": author,
        "user_id": user_id,
        "course_id": course_id,
        "book_status": book_status,
        "price": price,
        "location_id": location_id,
    }

    if location_detail is not None:
        post["location_detail"] = location_detail
    if original_price is not None:
        post["original_price"] = original_price
    if description is not None:
        post["description"] = description

    supabase.table("posts").insert(post).execute()


def update_post(
    id: int,
    status: str,
    book_title: str,
    author: str,
    course_id: int,
    book_status: str,
    price: int,
    location_id: int,
    location_detail: Optional[str] = None,
    original_price: Optional[int] = None,
    description: Optional[str] = None,
):
    supabase = get_supabase()

    post = {}

    if status is not None:
        post["status"] = status
    if book_title is not None:
        post["book_title"] = book_title
    if author is not None:
        post["author"] = author
    if course_id is not None:
        post["course_id"] = course_id
    if book_status is not None:
        post["book_status"] = book_status
    if price is not None:
        post["price"] = price
    if location_id is not None:
        post["location_id"] = location_id
    if location_detail is not None:
        post["location_detail"] = location_detail
    if original_price is not None:
        post["original_price"] = original_price
    if description is not None:
        post["description"] = description

    supabase.table("posts").update(post).eq("id", id).execute()


def delete_post(id: int):
    supabase = get_supabase()
    supabase.table("posts").delete().eq("id", id).execute()
