from fastapi import APIRouter
from app.schemas.posts import SearchRequest, SortBy
from app.crud.posts import search_posts


router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/search")
async def search_posts_route(search_request: SearchRequest):
    results = search_posts(status=search_request.status, book_title=search_request.book_title, author=search_request.author, publisher=search_request.publisher,
                           location=search_request.location, min_price=search_request.min_price, max_price=search_request.max_price)

    if search_request.sort_by == SortBy.NEWEST:
        results = sorted(results, key=lambda x: x["created_at"], reverse=True)
    elif search_request.sort_by == SortBy.PRICE_ASC:
        results = sorted(results, key=lambda x: x["price"])
    elif search_request.sort_by == SortBy.PRICE_DESC:
        results = sorted(results, key=lambda x: x["price"], reverse=True)

    return results[search_request.offset:search_request.offset + search_request.limit]
