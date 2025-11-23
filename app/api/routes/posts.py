from fastapi import APIRouter, Query, Depends, HTTPException
from app.schemas.posts import InsertUpdatePostRequest
from app.crud.posts import (
    get_posts_list,
    get_post,
    insert_post,
    update_post,
)
from typing import List, Optional
from app.utils.get_token import get_current_user_id


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/")
async def get_posts_list_route(
    status: Optional[List[str]] = Query(default=None),
    book_title: Optional[str] = None,
    author: Optional[str] = None,
    book_status: Optional[str] = None,
    course_id: Optional[int] = None,
    location_id: Optional[int] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    offset: Optional[int] = Query(default=0),
    limit: Optional[int] = Query(default=10)
):
    posts = get_posts_list(
        status=status,
        book_title=book_title,
        author=author,
        book_status=book_status,
        course_id=course_id,
        location_id=location_id,
        min_price=min_price,
        max_price=max_price
    )

    posts = [
        {
            "id": post["id"],
            "user_id": post["user_id"],
            "book_title": post["book_title"],
            "author": post["author"],
            "course_id": post["course_id"],
            "book_status": post["book_status"],
            "price": post["price"],
            "location_id": post["location_id"],
            "location_detail": post["location_detail"],
            "original_price": post["original_price"],
            "description": post["description"],
        }
        for post in posts[offset:offset + limit]]

    return posts


@router.get("/{post_id}")
async def get_post_route(post_id: int):
    post = get_post(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"id": post["id"], "book_title": post["book_title"], "author": post["author"], "course_id": post["course_id"], "book_status": post["book_status"], "price": post["price"], "location_id": post["location_id"], "location_detail": post["location_detail"], "original_price": post["original_price"], "description": post["description"]}


@router.post("/")
async def insert_post_route(insert_post_request: InsertUpdatePostRequest, user_id: str = Depends(get_current_user_id)):
    try:
        insert_post(
            book_title=insert_post_request.book_title,
            author=insert_post_request.author,
            course=insert_post_request.course.value,
            book_status=insert_post_request.book_status.value,
            price=insert_post_request.price,
            location=insert_post_request.location.value,
            location_detail=insert_post_request.location_detail,
            original_price=insert_post_request.original_price,
            description=insert_post_request.description,
            user_id=user_id
        )
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{post_id}")
async def update_post_route(post_id: int, update_post_request: InsertUpdatePostRequest):
    update_post(id=post_id, book_title=update_post_request.book_title, author=update_post_request.author, course=update_post_request.course.value, book_status=update_post_request.book_status.value, price=update_post_request.price,
                location=update_post_request.location.value, location_detail=update_post_request.location_detail, original_price=update_post_request.original_price, description=update_post_request.description)
    return {"ok": True}
