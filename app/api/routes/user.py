from fastapi import APIRouter, Depends
from app.utils.get_token import get_current_user_id

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me")
def get_my_profile_route(user_id: str = Depends(get_current_user_id)):
    from app.crud.profiles import get_profile
    from app.crud.posts import get_posts_list
    from app.crud.orders import get_orders_list

    my_profile = get_profile(user_id=user_id)
    count_posts = len(get_posts_list(seller_id=user_id))
    count_bought_orders = len(get_orders_list(buyer_id=user_id))
    count_sold_orders = len(get_orders_list(seller_id=user_id))

    return {
        **my_profile,
        "count_posts": count_posts,
        "count_orders": count_bought_orders,
        "count_sold_orders": count_sold_orders,
    }


@router.get("/posts")
def get_my_posts_route(user_id: str = Depends(get_current_user_id)):
    from app.crud.posts import get_posts_list
    posts = get_posts_list(seller_id=user_id)
    return posts


@router.get("/orders")
def get_my_orders_route(user_id: str = Depends(get_current_user_id)):
    from app.crud.orders import get_orders_list
    orders = get_orders_list(seller_id=user_id)
    return orders
