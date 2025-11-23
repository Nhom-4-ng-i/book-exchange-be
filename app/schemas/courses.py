from pydantic import BaseModel


class InsertUpdateCourseRequest(BaseModel):
    name: str
