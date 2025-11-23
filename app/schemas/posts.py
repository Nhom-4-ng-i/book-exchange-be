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


class InsertUpdatePostRequest(BaseModel):
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
