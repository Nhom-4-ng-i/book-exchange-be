from fastapi import APIRouter
from app.crud.courses import (
    get_courses_list,
    get_course,
    insert_course,
    update_course,
    delete_course
)
from app.schemas.courses import InsertUpdateCourseRequest


router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("/")
async def get_courses_list_route():
    courses = get_courses_list()
    courses = [{"id": course["id"], "name": course["name"]}
               for course in courses]
    return courses


@router.get("/{course_id}")
async def get_course_route(course_id: int):
    course = get_course(id=course_id)
    return {"id": course["id"], "name": course["name"]}


@router.post("/")
async def insert_course_route(course_request: InsertUpdateCourseRequest):
    name = course_request.name
    insert_course(name=name)


@router.put("/{course_id}")
async def update_course_route(course_id: int, course_request: InsertUpdateCourseRequest):
    name = course_request.name
    update_course(id=course_id, name=name)


@router.delete("/{course_id}")
async def delete_course_route(course_id: int):
    delete_course(id=course_id)
