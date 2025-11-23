from fastapi import APIRouter
from app.crud.courses import get_all_courses


router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("/")
async def get_all_courses_route():
    courses = get_all_courses()
    courses = [course["name"] for course in courses]
    return courses
