from app.services.supabase import get_supabase
from typing import Optional, List
import datetime


def get_orders_list(
    buyer_id: Optional[str] = None,
    seller_id: Optional[str] = None,
    status_code: Optional[List[str]] = None,
    post_id: Optional[int] = None,
):
    supabase = get_supabase()

    query = (
        supabase
        .table("orders")
        .select(
            """
            id,
            created_at,
            order_status!inner(code, name),
            buyer:profiles!buyer_id(name, phone),
            posts!inner(
                book_title,
                author,
                price,
                avatar_url,
                seller_id,
                courses!inner(name),
                locations!inner(name),
                book_status!inner(name),
                post_status!inner(name),
                profiles!inner(name)
            )
            """
        )
    )

    if buyer_id:
        query = query.eq("buyer_id", buyer_id)

    if seller_id:
        query = query.eq("posts.seller_id", seller_id)

    if status_code:
        query = query.in_("order_status.code", status_code)

    if post_id:
        query = query.eq("posts.id", post_id)

    response = query.execute()
    raw_orders = response.data or []

    orders = []
    for row in raw_orders:
        post = row["posts"]

        orders.append({
            "order_id": row.get("id"),
            "order_time": datetime.datetime.fromisoformat(row.get("created_at")).strftime("%d/%m/%Y %H:%M:%S"),
            "order_status": row.get("order_status", {}).get("name") if row.get("order_status") else None,
            "order_status_code": row.get("order_status", {}).get("code") if row.get("order_status") else None,
            "title": post["book_title"],
            "author": post["author"],
            "price": post["price"],
            "avatar_url": post.get("avatar_url"),
            "course": post.get("courses", {}).get("name") if post.get("courses") else None,
            "location": post.get("locations", {}).get("name") if post.get("locations") else None,
            "book_status": post.get("book_status", {}).get("name") if post.get("book_status") else None,
            "book_status_code": post.get("book_status", {}).get("code") if post.get("book_status") else None,
            "post_status": post.get("post_status", {}).get("name") if post.get("post_status") else None,
            "post_status_code": post.get("post_status", {}).get("code") if post.get("post_status") else None,
            "seller_name": post.get("profiles", {}).get("name") if post.get("profiles") else None,
            "seller_phone": post.get("profiles", {}).get("phone") if post.get("profiles") else None,
            "buyer_name": row.get("buyer", {}).get("name") if row.get("buyer") else None,
            "buyer_phone": row.get("buyer", {}).get("phone") if row.get("buyer") else None,
        })

    return orders


def insert_order(post_id: int, buyer_id: str, buyer_note: Optional[str] = None):
    supabase = get_supabase()
    (
        supabase
        .table("orders")
        .insert({
            "post_id": post_id,
            "buyer_id": buyer_id,
            "buyer_note": buyer_note
        })
        .execute()
    )


def update_order(order_id: int, status_id: int):
    supabase = get_supabase()
    response = (
        supabase
        .table("orders")
        .update({
            "status_id": status_id
        })
        .eq("id", order_id)
        .execute()
    )
    return response.data
