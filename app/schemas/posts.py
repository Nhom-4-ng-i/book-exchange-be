from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from datetime import datetime


class SortBy(Enum):
    NEWEST = "newest"
    PRICE_ASC = "price_asc"
    PRICE_DESC = "price_desc"


class Status(Enum):
    ACTIVE = "active"
    SOLD = "sold"
    TRADING = "trading"


class Location(Enum):
    HCMUT = "hcmut"
    HCMUS = "hcmus"
    HCMUTE = "hcmute"
    FTU = "ftu"


class BookStatus(Enum):
    UNUSED = "Mới - chưa sử dụng"
    UNREAD = "Chưa đọc - nguyên seal"
    USED = "Khá - đã sử dụng ít"
    DAMAGED = "Rách - có dấu hiệu cũ"


class InsertPostRequest(BaseModel):
    book_title: str
    author: str
    course: str
    book_status: BookStatus
    price: int
    original_price: Optional[int] = None
    description: Optional[str] = None
    location: Location
    location_detail: Optional[str] = None
    avatar_url: Optional[str] = None
    user_id: Optional[str] = None


class SearchRequest(BaseModel):
    status: List[Status] = [Status.ACTIVE]
    book_title: Optional[str] = None
    author: Optional[str] = None
    course: Optional[str] = None
    book_status: Optional[BookStatus] = None
    location: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    sort_by: SortBy = SortBy.NEWEST
    offset: int = 0
    limit: int = 10


class PostDetailResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    price: float
    created_at: Optional[str] = None
    seller_name: Optional[str] = None
    author: Optional[str] = None
    course: Optional[str] = None
    location: Optional[str] = None
    status: Optional[Status] = None
    book_status: Optional[BookStatus] = None
    original_price: Optional[float] = None
    location_detail: Optional[str] = None
    avatar: Optional[str] = None
