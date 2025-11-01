from pydantic import BaseModel, EmailStr

# Sign Up
class SignUpRequest(BaseModel):
    email: EmailStr
    name: str


# Sign In
class SignInRequest(BaseModel):
    email: EmailStr

class SignInResponse(BaseModel):
    access_token: str
    id: str
    email: EmailStr
    name: str
    role: str