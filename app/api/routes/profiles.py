from fastapi import APIRouter
from app.crud.profiles import get_profile_by_id


router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/{user_id}")
async def get_profile_route(user_id: str):
    response = get_profile_by_id(user_id=user_id)
    return response
