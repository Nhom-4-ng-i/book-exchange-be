from fastapi import APIRouter, Depends
from app.utils.get_token import get_current_user_id
from app.crud.courses import get_courses_list


router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("/")
async def get_courses_list_route(_: str = Depends(get_current_user_id)):
    courses = get_courses_list()
    return courses
