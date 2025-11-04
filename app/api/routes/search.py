from fastapi import APIRouter
from app.schemas.search import SearchRequest


router = APIRouter(prefix="/search", tags=["search"])


@router.get("/")
async def search(query: SearchRequest):
    pass
