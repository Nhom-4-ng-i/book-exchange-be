from typing import Optional, List, Any
from app.services.supabase import get_supabase
from app.schemas.posts import Status, BookStatus, Location
from app.services.cloudinary_client import upload_image_to_cloudinary

from app.schemas.posts import Status
from typing import Optional
from datetime import datetime


def get_post_by_id(post_id: int):
    supabase = get_supabase()
    # fetch post
    res = (
        supabase
        .table("posts")
        .select("*")
        .eq("post_id", post_id)
        .single()
        .execute()
    )
    post = res.data
    if not post:
        return None

    seller_name = None
    user_id = post.get("user_id")
    if user_id:
        try:
            profile_res = (
                supabase
                .table("profiles")
                .select("name")
                .eq("user_id", user_id)
                .single()
                .execute()
            )
            profile = profile_res.data
            if profile:
                # prefer 'name' field, fallback to 'full_name' if present
                seller_name = profile.get("name")
        except Exception:
            seller_name = None

    # attach seller_name to returned post dict
    post["seller_name"] = seller_name
    return post


def insert_post(book_title: str, author: str, course: str, book_status: BookStatus, price: int, location: Location, location_detail: Optional[str] = None, original_price: Optional[int] = None, description: Optional[str] = None, avatar: Optional[Any] = None, user_id: Optional[str] = None):
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


def search_posts(status: List[Status], book_title: Optional[str] = None, author: Optional[str] = None, course: Optional[str] = None, book_status: Optional[BookStatus] = None, location: Optional[Location] = None, min_price: Optional[int] = None, max_price: Optional[int] = None):
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


def get_post_detail(post_id: int) -> Optional[dict]:

    supabase = get_supabase()
    try:
        resp = supabase.table('posts').select(
            '*').eq('post_id', post_id).limit(1).execute()
    except Exception:
        return None

    data = getattr(resp, 'data', None) or []
    if not data:
        return None

    post = data[0]

    # seller id
    seller_id = post.get('user_id')
    seller_name = ''
    if seller_id:
        try:
            s = supabase.table('profiles').select('name').eq(
                'user_id', seller_id).limit(1).execute()
            sdata = getattr(s, 'data', None) or []
            if sdata:
                seller = sdata[0]
                seller_name = seller.get('full_name') or seller.get(
                    'name') or seller.get('username') or ''
        except Exception:
            seller_name = ''

    # Map field
    title = post.get('book_title') or ''
    author = post.get('author') or ''
    course = post.get('course') or ''
    location = post.get('location') or ''
    description = post.get('description') or ''
    price = post.get('price') or 0
    status = post.get('status') or ''
    book_status = post.get('book_status') or ''
    original_price = post.get('original_price') or 0
    location_detail = post.get('location_detail') or ''
    # image_url
    avatar = post.get('avatar') or ''
    created_at = post.get('created_at')
    return {
        'id': post.get('post_id'),
        'title': title,
        'description': description,
        'price': float(price) if price is not None else 0.0,
        'created_at': created_at,
        'seller_name': seller_name,
        'author': author,
        'course': course,
        'location': location,
        'status': status,
        'book_status': book_status,
        'original_price': float(original_price) if original_price is not None else 0.0,
        'location_detail': location_detail,
        'avatar': avatar
    }
