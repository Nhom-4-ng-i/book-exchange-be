from fastapi import APIRouter, Depends
from typing import List
from app.utils.get_token import get_current_user_id
from app.schemas.wishlists import WishlistResponse

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me")
async def get_my_profile_route(user_id: str = Depends(get_current_user_id)):
    from app.crud.profiles import get_profile
    from app.crud.posts import get_posts_list
    from app.crud.orders import get_orders_list

    my_profile = get_profile(user_id=user_id)
    count_posts = len(get_posts_list(seller_id=user_id, status=["PENDING", "TRADING", "SOLD"]))
    count_bought_orders = len(get_posts_list(seller_id=user_id, status="SOLD"))
    count_sold_orders = len(get_orders_list(seller_id=user_id, status="COMPLETED"))

    return {
        **my_profile,
        "count_posts": count_posts,
        "count_orders": count_bought_orders,
        "count_sold_orders": count_sold_orders,
    }


@router.get("/posts")
async def get_my_posts_route(user_id: str = Depends(get_current_user_id)):
    from app.crud.posts import get_posts_list
    posts = get_posts_list(seller_id=user_id)
    return posts


@router.get("/orders")
async def get_my_orders_route(user_id: str = Depends(get_current_user_id)):
    from app.crud.orders import get_orders_list
    orders = get_orders_list(buyer_id=user_id)
    return orders


@router.get("/wishlists", response_model=List[WishlistResponse])
async def get_my_wishlists_route(user_id: str = Depends(get_current_user_id)):
    from app.crud.wishlists import get_wishlists_list
    wishlists = get_wishlists_list(user_id=user_id)
    return wishlists
