from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


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


class Course(Enum):
    CALCULUS1 = "Giải tích 1"
    CALCULUS2 = "Giải tích 2"
    CALCULUS3 = "Giải tích 3"
    LINEAR_ALGEBRA = "Đại số tuyến tính"
    PROBABILITY_AND_STATISTICS = "Xác suất và thống kê"
    DISCRETE_MATHEMATICS = "Toán rời rạc"
    DATABASE_SYSTEM = "Hệ cơ sở dữ liệu"
    OPERATING_SYSTEM = "Hệ điều hành"
    COMPUTER_NETWORK = "Mạng máy tính"
    COMPUTER_ARCHITECTURE = "Kiến trúc máy tính"


class InsertPostRequest(BaseModel):
    book_title: str
    author: str
    publisher: str
    location: Location
    price: int
    original_price: Optional[int] = None
    book_status: BookStatus


class SearchRequest(BaseModel):
    status: List[Status] = [Status.ACTIVE]
    book_title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    location: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    sort_by: SortBy = SortBy.NEWEST
    offset: int = 0
    limit: int = 10
