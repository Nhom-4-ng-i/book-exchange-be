from pydantic import BaseModel


class InsertUpdateLocationRequest(BaseModel):
    name: str
