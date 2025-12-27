from typing import Optional, List
from app.services.supabase import get_supabase


def _base_posts_query(supabase):
    return (
        supabase
        .table("posts")
        .select(
            """
            *,
            courses!inner(name),
            locations!inner(name),
            book_status!inner(code, name),
            post_status!inner(code, name),
            profiles!inner(name)
            """
        )
    )


def _map_post_row(row: dict) -> dict:
    return {
        "id": row["id"],
        "status": (row.get("post_status") or {}).get("name"),
        "status_code": (row.get("post_status") or {}).get("code"),
        "book_title": row["book_title"],
        "author": row["author"],
        "course": (row.get("courses") or {}).get("name"),
        "location": (row.get("locations") or {}).get("name"),
        "book_status": (row.get("book_status") or {}).get("name"),
        "price": row["price"],
        "created_at": row["created_at"],
        "avatar_url": row.get("avatar_url"),
        "original_price": row["original_price"],
        "description": row["description"],
        "location_detail": row["location_detail"],
        "seller_name": (row.get("profiles") or {}).get("name"),
    }


def get_posts_list(
    status_code: Optional[List[str]] = None,
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

    query = _base_posts_query(supabase)

    if status_code is not None:
        query = query.in_("post_status.code", status_code)

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
        query = query.eq("seller_id", seller_id)
        
    if book_title is not None:
        query = query.text_search("book_title", f"'{book_title}'")

    response = query.execute()
    raw_posts = response.data or []

    posts = [_map_post_row(row) for row in raw_posts]
    return posts


def get_post(id: int):
    supabase = get_supabase()

    query = (
        _base_posts_query(supabase)
        .eq("id", id)
        .single()
    )
    response = query.execute()
    row = response.data

    if row is None:
        return None

    return _map_post_row(row)


def insert_post(
    seller_id: str,
    status_id: int,
    book_title: str,
    author: str,
    course_id: int,
    book_status_id: int,
    price: int,
    location_id: int,
    location_detail: Optional[str],
    original_price: Optional[int],
    description: Optional[str],
    avatar_url: Optional[str] = None,
):
    supabase = get_supabase()

    post = {
        "book_title": book_title,
        "status_id": status_id,
        "author": author,
        "seller_id": seller_id,
        "course_id": course_id,
        "book_status_id": book_status_id,
        "price": price,
        "location_id": location_id,
    }

    if location_detail is not None:
        post["location_detail"] = location_detail
    if original_price is not None:
        post["original_price"] = original_price
    if description is not None:
        post["description"] = description
    if avatar_url is not None:
        post["avatar_url"] = avatar_url

    supabase.table("posts").insert(post).execute()


def update_post(
    post_id: int,
    status_id: Optional[int] = None,
    book_title: Optional[str] = None,
    author: Optional[str] = None,
    course_id: Optional[int] = None,
    book_status_id: Optional[int] = None,
    price: Optional[int] = None,
    location_id: Optional[int] = None,
    location_detail: Optional[str] = None,
    original_price: Optional[int] = None,
    description: Optional[str] = None,
    avatar_url: Optional[str] = None,
):
    supabase = get_supabase()

    post = {}

    if status_id is not None:
        post["status_id"] = status_id
    if book_title is not None:
        post["book_title"] = book_title
    if author is not None:
        post["author"] = author
    if course_id is not None:
        post["course_id"] = course_id
    if book_status_id is not None:
        post["book_status_id"] = book_status_id
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
    if avatar_url is not None:  
        post["avatar_url"] = avatar_url

    if post:
        supabase.table("posts").update(post).eq("id", post_id).execute()