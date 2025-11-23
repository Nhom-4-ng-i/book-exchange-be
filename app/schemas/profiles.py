from pydantic import BaseModel


class InsertProfileRequest(BaseModel):
    user_id: str
    name: str
    email: str


class UpdateProfileRequest(BaseModel):
    name: str
    email: str
