from fastapi import APIRouter, Depends
from app.crud.orders import (
    get_orders_list,
    get_order,
    insert_order,
    update_order,
    delete_order
)
from app.crud.posts import update_post
from app.schemas.orders import InsertOrderRequest, UpdateOrderRequest
from app.utils.get_token import get_current_user_id


router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/")
async def get_orders_list_route():
    orders = get_orders_list()
    orders = [
        {
            "id": order["id"],
            "post_id": order["post_id"],
            "buyer_id": order["buyer_id"],
            "buyer_note": order["buyer_note"],
            "status": order["status"],
        }
        for order in orders
    ]
    return orders


@router.get("/{order_id}")
async def get_order_route(order_id: int):
    order = get_order(order_id=order_id)
    return {
        "id": order["id"],
        "post_id": order["post_id"],
        "buyer_id": order["buyer_id"],
        "buyer_note": order["buyer_note"],
        "status": order["status"],
    }


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


# @router.put("/{order_id}")
# async def update_order_route(order_id: int, order_request: UpdateOrderRequest):
#     update_order(
#         order_id=order_id,
#         status_id=order_request.status_id
#     )


# @router.delete("/{order_id}")
# async def delete_order_route(order_id: int):
#     delete_order(order_id=order_id)
