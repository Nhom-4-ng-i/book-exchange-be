from pydantic import BaseModel
from typing import Optional


class InsertPostRequest(BaseModel):
    book_title: str
    author: str
    course_id: int
    book_status: str
    price: int
    location_id: int
    original_price: Optional[int] = None
    description: Optional[str] = None
    location_detail: Optional[str] = None
    avatar_url: Optional[str] = None


class UpdatePostRequest(BaseModel):
    book_title: Optional[str] = None
    status: Optional[str] = None
    author: Optional[str] = None
    course_id: Optional[int] = None
    book_status: Optional[str] = None
    price: Optional[int] = None
    location_id: Optional[int] = None
    original_price: Optional[int] = None
    description: Optional[str] = None
    location_detail: Optional[str] = None
    avatar_url: Optional[str] = None
