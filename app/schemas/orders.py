from pydantic import BaseModel
from typing import Optional


class InsertOrderRequest(BaseModel):
    post_id: int
    buyer_note: Optional[str] = None
