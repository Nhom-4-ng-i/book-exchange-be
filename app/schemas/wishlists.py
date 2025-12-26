from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InsertWishlistRequest(BaseModel):
    title: str
    course_id: int
    max_price: int


class UpdateWishlistRequest(BaseModel):
    title: Optional[str] = None
    course_id: Optional[int] = None
    max_price: Optional[int] = None


class WishlistResponse(BaseModel):
    id: int
    created_at: datetime
    title: str
    course_id: int
    name_course: Optional[str] = None
    max_price: int
    user_id: str