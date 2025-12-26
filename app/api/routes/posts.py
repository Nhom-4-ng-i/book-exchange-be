from fastapi import APIRouter, Query, Depends
from app.utils.get_token import get_current_user_id
from app.schemas.posts import InsertPostRequest, UpdatePostRequest
from app.crud.posts import (
    get_posts_list,
    get_post,
    insert_post,
    update_post
)
from app.crud.orders import (
    get_orders_list,
    update_order
)
from app.crud.wishlists import get_wishlists_list
from app.crud.notifications import insert_notification
from typing import List, Optional


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/")
async def get_posts_list_route(
    book_title: Optional[str] = Query(default=None),
    author: Optional[str] = Query(default=None),
    book_status: Optional[str] = Query(default=None),
    course_id: Optional[int] = Query(default=None),
    location_id: Optional[int] = Query(default=None),
    min_price: Optional[int] = Query(default=None),
    max_price: Optional[int] = Query(default=None),
    sort_by: Optional[str] = Query(default=None),
    offset: Optional[int] = Query(default=None),
    limit: Optional[int] = Query(default=None),
    _: str = Depends(get_current_user_id),
):
    posts = get_posts_list(
        status="PENDING",
        book_title=book_title,
        author=author,
        book_status=book_status,
        course_id=course_id,
        location_id=location_id,
        min_price=min_price,
        max_price=max_price
    )

    if sort_by is not None:
        if sort_by == "newest":
            posts = sorted(posts, key=lambda x: x["created_at"], reverse=True)
        elif sort_by == "price_asc":
            posts = sorted(posts, key=lambda x: x["price"])
        elif sort_by == "price_desc":
            posts = sorted(posts, key=lambda x: x["price"], reverse=True)

    if offset is not None:
        if limit is not None:
            posts = posts[offset:offset + limit]
        else:
            posts = posts[offset:]

    posts = [
        {
            "id": post["id"],
            "status": post["status"],
            "seller_name": post["seller_name"],
            "title": post["book_title"],
            "author": post["author"],
            "price": post["price"],
            "course": post["course"],
            "location": post["location"],
            "book_status": post["book_status"],
            "original_price": post["original_price"],
            "description": post["description"],
            "location_detail": post["location_detail"],
            "avatar_url": post["avatar_url"],
        }
        for post in posts]

    return posts


@router.get("/{post_id}")
async def get_post_route(post_id: int, _: str = Depends(get_current_user_id)):
    post = get_post(id=post_id)
    return post


@router.post("/")
async def insert_post_route(insert_post_request: InsertPostRequest, user_id: str = Depends(get_current_user_id)):
    insert_post(
        seller_id=user_id,
        status_id=1,
        book_title=insert_post_request.book_title,
        author=insert_post_request.author,
        course_id=insert_post_request.course_id,
        book_status_id=insert_post_request.book_status_id,
        price=insert_post_request.price,
        location_id=insert_post_request.location_id,
        location_detail=insert_post_request.location_detail,
        original_price=insert_post_request.original_price,
        description=insert_post_request.description
    )
    
    # Check wishlists
    wishlists = get_wishlists_list(
        book_title=insert_post_request.book_title,
        course_id=insert_post_request.course_id,
        max_price=insert_post_request.price,
        seller_id=user_id,
    )
    for wishlist in wishlists:
        insert_notification(user_id=wishlist["user_id"], title="WISHLIST", type_id=1, content=f"Đã tìm thấy bài đăng có sách {insert_post_request.book_title} bạn cần.")


@router.post("/{post_id}/cancel")
async def cancel_post_route(post_id: int, _: str = Depends(get_current_user_id)):
    orders = get_orders_list(post_id=post_id, status="PENDING")
    for order in orders:
        update_order(order_id=order["order_id"], status_id=3)
    update_post(post_id=post_id, status_id=4)


@router.put("/{post_id}")
async def update_post_route(post_id: int, update_post_request: UpdatePostRequest, _: str = Depends(get_current_user_id)):
    update_post(
        post_id=post_id,
        book_title=update_post_request.book_title,
        author=update_post_request.author,
        course_id=update_post_request.course_id,
        book_status_id=update_post_request.book_status_id,
        price=update_post_request.price,
        location_id=update_post_request.location_id,
        location_detail=update_post_request.location_detail,
        original_price=update_post_request.original_price,
        description=update_post_request.description
    )
