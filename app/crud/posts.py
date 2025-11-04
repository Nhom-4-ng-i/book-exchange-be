from app.services.supabase import get_supabase
from app.schemas.posts import Status
from typing import Optional
from datetime import datetime

def search_posts(status: Status, book_title: str, author: str, publisher: str, location: str, min_price: int, max_price: int):
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
        if publisher:
            response = [x for x in response if x["publisher"] == publisher]
        if location:
            response = [x for x in response if x["location"] == location]
        if min_price:
            response = [x for x in response if x["price"] >= min_price]
        if max_price:
            response = [x for x in response if x["price"] <= max_price]
        return response

    # Get all posts with status
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
        resp = supabase.table('posts').select('*').eq('post_id', post_id).limit(1).execute()
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
            s = supabase.table('profiles').select('name').eq('user_id', seller_id).limit(1).execute()
            sdata = getattr(s, 'data', None) or []
            if sdata:
                seller = sdata[0]
                seller_name = seller.get('full_name') or seller.get('name') or seller.get('username') or ''
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