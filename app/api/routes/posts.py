from fastapi import APIRouter, Depends, HTTPException
from app.schemas.posts import SearchRequest, InsertPostRequest, SortBy
from app.crud.posts import search_posts, insert_post, get_post_by_id, get_post_detail
from app.schemas.posts import PostDetailResponse
from app.utils.get_token import get_current_user_id


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/{post_id}")
async def get_post_route(post_id: int):
    response = get_post_by_id(post_id=post_id)
    return response


@router.post("/")
async def insert_post_route(insert_post_request: InsertPostRequest, user_id: str = Depends(get_current_user_id)):
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


@router.post("/search")
async def search_posts_route(search_request: SearchRequest):
    results = search_posts(
        status=search_request.status,
        book_title=search_request.book_title,
        author=search_request.author,
        course=search_request.course.value,
        book_status=search_request.book_status.value,
        location=search_request.location.value,
        min_price=search_request.min_price,
        max_price=search_request.max_price
    )

    if search_request.sort_by == SortBy.NEWEST:
        results = sorted(results, key=lambda x: x["created_at"], reverse=True)
    elif search_request.sort_by == SortBy.PRICE_ASC:
        results = sorted(results, key=lambda x: x["price"])
    elif search_request.sort_by == SortBy.PRICE_DESC:
        results = sorted(results, key=lambda x: x["price"], reverse=True)

    return results[search_request.offset:search_request.offset + search_request.limit]


@router.get("/{post_id}", response_model=PostDetailResponse)
def read_post_detail(post_id: int):
    """Return detailed information about a single post by id.

    Uses `get_post_detail` from the CRUD layer which queries Supabase.
    """
    post = get_post_detail(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
