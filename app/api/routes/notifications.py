from fastapi import APIRouter, Depends
from app.utils.get_token import get_current_user_id
from app.crud.notifications import get_notifications_list, update_notification

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/")
async def get_notifications_list_route(user_id: str = Depends(get_current_user_id)):
    notifications = get_notifications_list(user_id=user_id)
    return notifications


@router.post("/{notification_id}/read")
async def read_notification_route(notification_id: int, user_id: str = Depends(get_current_user_id)):
    update_notification(notification_id=notification_id,
                        user_id=user_id, is_read=True)


@router.post("/read-all")
async def read_all_notifications_route(user_id: str = Depends(get_current_user_id)):
    update_notification(user_id=user_id, is_read=True)
