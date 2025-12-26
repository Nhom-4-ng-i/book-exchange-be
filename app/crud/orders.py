from app.services.supabase import get_supabase
from typing import Optional


def get_orders_list(
    buyer_id: Optional[str] = None,
    seller_id: Optional[str] = None,
    status: Optional[str] = None,
    post_id: Optional[int] = None,
):
    supabase = get_supabase()

    # Cập nhật query: Lấy thêm status_id và thông tin ng mua
    query = (
        supabase
        .table("orders")
        .select(
            """
            id,
            created_at,
            status_id,
            order_status(code, name),
            buyer:profiles!buyer_id(name, phone), 
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
        .order("created_at", desc=True)
    )

    if buyer_id:
        query = query.eq("buyer_id", buyer_id)

    if seller_id:
        query = query.eq("posts.seller_id", seller_id)

    if status:
        query = query.eq("order_status.code", status)

    if post_id:
        query = query.eq("posts.id", post_id)

    response = query.execute()
    raw_orders = response.data or []

    orders = []
    for row in raw_orders:
        post = row["posts"]
        buyer = row.get("buyer") or {}

        orders.append({
            "order_id": row.get("id"),
            "created_at": row.get("created_at"),
            "status_id": row.get("status_id"),
            "order_status": row.get("order_status", {}).get("name"),
            
            # Thông tin người mua
            "buyer_name": buyer.get("name"),
            "buyer_phone": buyer.get("phone"),

            # Thông tin bài đăng
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
