from fastapi import APIRouter, Depends
from app.utils.get_token import get_current_user_id
from app.crud.locations import get_locations_list


router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/")
async def get_locations_list_route(_: str = Depends(get_current_user_id)):
    locations = get_locations_list()
    return locations
