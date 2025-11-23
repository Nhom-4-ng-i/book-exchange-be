from fastapi import APIRouter
from app.crud.courses import get_all_courses, get_course_name_by_id, get_course_id_by_name, insert_course, update_course_by_id, update_course_by_name, delete_course_by_id, delete_course_by_name
from app.schemas.courses import InsertUpdateCourseRequest


router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("/")
async def get_all_courses_route():
    courses = get_all_courses()
    courses = [course["name"] for course in courses]
    return courses


@router.get("/{course_id}")
async def get_course_name_by_id_route(course_id: int):
    course = get_course_name_by_id(course_id=course_id)
    return course


@router.get("/{course_name}")
async def get_course_id_by_name_route(course_name: str):
    course = get_course_id_by_name(course_name=course_name)
    return course


@router.post("/")
async def insert_course_route(course_request: InsertUpdateCourseRequest):
    name = course_request.name
    insert_course(name=name)


@router.put("/{course_id}")
async def update_course_by_id_route(course_id: int, course_request: InsertUpdateCourseRequest):
    name = course_request.name
    update_course_by_id(course_id=course_id, name=name)


@router.put("/{course_name}")
async def update_course_by_name_route(course_name: str, course_request: InsertUpdateCourseRequest):
    name = course_request.name
    update_course_by_name(course_name=course_name, name=name)


@router.delete("/{course_id}")
async def delete_course_by_id_route(course_id: int):
    delete_course_by_id(course_id=course_id)


@router.delete("/{course_name}")
async def delete_course_by_name_route(course_name: str):
    delete_course_by_name(course_name=course_name)
