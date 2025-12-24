from app.services.supabase import get_supabase


def get_notifications_list(user_id: str):
    supabase = get_supabase()
    response = (
        supabase
        .table("notifications")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    return response.data


def update_notification(user_id: str, is_read: bool, notification_id: int = None):
    supabase = get_supabase()
    if notification_id is not None:
        (
            supabase
            .table("notifications")
            .update({"is_read": is_read})
            .eq("id", notification_id)
            .eq("user_id", user_id)
            .execute()
        )
    else:
        (
            supabase
            .table("notifications")
            .update({"is_read": is_read})
            .eq("user_id", user_id)
            .execute()
        )
