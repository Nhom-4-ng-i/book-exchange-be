from pydantic import BaseModel
from typing import Optional


class InsertWishlistRequest(BaseModel):
    title: str
    course_id: int
    max_price: int


class UpdateWishlistRequest(BaseModel):
    title: Optional[str] = None
    course_id: Optional[int] = None
    max_price: Optional[int] = None
