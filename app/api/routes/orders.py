from fastapi import APIRouter, Depends
from app.crud.orders import insert_order, update_order
from app.crud.posts import update_post
from app.schemas.orders import InsertOrderRequest
from app.utils.get_token import get_current_user_id


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/")
async def insert_order_route(order_request: InsertOrderRequest, user_id: str = Depends(get_current_user_id)):
    insert_order(
        post_id=order_request.post_id,
        buyer_id=user_id,
        buyer_note=order_request.buyer_note
    )


@router.post("/{order_id}/accept")
async def accept_order_route(order_id: int, _: str = Depends(get_current_user_id)):
    response = update_order(order_id=order_id, status_id=2)
    update_post(post_id=response["post_id"], status_id=2)


@router.post("/{order_id}/reject")
async def reject_order_route(order_id: int, _: str = Depends(get_current_user_id)):
    update_order(order_id=order_id, status_id=3)


@router.post("/{order_id}/complete")
async def complete_order_route(order_id: int, _: str = Depends(get_current_user_id)):
    response = update_order(order_id=order_id, status_id=4)
    update_post(post_id=response["post_id"], status_id=3)


@router.post("/{order_id}/cancel")
async def cancel_order_route(order_id: int, _: str = Depends(get_current_user_id)):
    update_order(order_id=order_id, status_id=5)
