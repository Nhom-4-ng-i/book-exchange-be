from pydantic import BaseModel


class InsertOrderRequest(BaseModel):
    post_id: int


class UpdateOrderRequest(BaseModel):
    status: str
