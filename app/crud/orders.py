from app.services.supabase import get_supabase


def get_orders_list():
    supabase = get_supabase()
    res = (
        supabase
        .table("orders")
        .select("*")
        .execute()
    )
    return res.data


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


def insert_order(post_id: int, buyer_id: str):
    supabase = get_supabase()
    (
        supabase
        .table("orders")
        .insert({
            "post_id": post_id,
            "buyer_id": buyer_id,
            "status": "pending"
        })
        .execute()
    )


def update_order(order_id: int, status: str):
    supabase = get_supabase()
    (
        supabase
        .table("orders")
        .update({
            "status": status
        })
        .eq("id", order_id)
        .execute()
    )


def delete_order(order_id: int):
    supabase = get_supabase()
    (
        supabase
        .table("orders")
        .delete()
        .eq("id", order_id)
        .execute()
    )
