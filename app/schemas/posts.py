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
