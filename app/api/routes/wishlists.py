from fastapi import APIRouter, Depends
from app.utils.get_token import get_current_user_id
from app.crud.wishlists import insert_wishlist, update_wishlist, delete_wishlist
from app.schemas.wishlists import InsertWishlistRequest, UpdateWishlistRequest

router = APIRouter(prefix="/wishlists", tags=["wishlists"])


@router.post("/")
async def insert_wishlist_route(wishlist_request: InsertWishlistRequest, user_id: str = Depends(get_current_user_id)):
    insert_wishlist(
        user_id=user_id,
        title=wishlist_request.title,
        course_id=wishlist_request.course_id,
        max_price=wishlist_request.max_price,
    )


@router.put("/{wishlist_id}")
async def update_wishlist_route(wishlist_id: int, wishlist_request: UpdateWishlistRequest, user_id: str = Depends(get_current_user_id)):
    update_wishlist(
        user_id=user_id,
        wishlist_id=wishlist_id,
        title=wishlist_request.title,
        course_id=wishlist_request.course_id,
        max_price=wishlist_request.max_price,
    )


@router.delete("/{wishlist_id}")
async def delete_wishlist_route(wishlist_id: int, user_id: str = Depends(get_current_user_id)):
    delete_wishlist(user_id=user_id, wishlist_id=wishlist_id)
