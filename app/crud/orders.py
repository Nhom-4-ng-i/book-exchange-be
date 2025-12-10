from app.services.supabase import get_supabase
from typing import Optional


def get_orders_list(
    buyer_id: Optional[str] = None,
    seller_id: Optional[str] = None,
    status: Optional[str] = None
):
    supabase = get_supabase()

    query = (
        supabase
        .table("orders")
        .select(
            """
            created_at,
            order_status(code, name),
            posts!inner(
                book_title,
                author,
                price,
                avatar_url,
                seller_id,
                courses(name),
                locations(name),
                book_status(name),
                post_status(name),
                profiles(name)
            )
            """
        )
    )

    if buyer_id:
        query = query.eq("buyer_id", buyer_id)

    if seller_id:
        query = query.eq("posts.seller_id", seller_id)

    if status:
        query = query.eq("order_status.code", status)

    response = query.execute()
    raw_orders = response.data or []

    orders = []
    for row in raw_orders:
        post = row["posts"]

        orders.append({
            "created_at": row.get("created_at"),
            "order_status": row["order_status"]["name"],
            "title": post["book_title"],
            "author": post["author"],
            "price": post["price"],
            "avatar_url": post.get("avatar_url"),
            "course": post.get("courses", {}).get("name"),
            "location": post.get("locations", {}).get("name"),
            "book_status": post.get("book_status", {}).get("name"),
            "post_status": post.get("post_status", {}).get("name"),
            "seller_name": post.get("profiles", {}).get("name"),
        })

    return orders


def get_order(order_id: int):
    supabase = get_supabase()
    res = (
        supabase
        .table("orders")
        .select("*")
        .eq("id", order_id)
        .single()
        .execute()
    )
    return res.data


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
    return response.data[0]


def delete_order(order_id: int):
    supabase = get_supabase()
    (
        supabase
        .table("orders")
        .delete()
        .eq("id", order_id)
        .execute()
    )
