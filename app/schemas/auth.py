from pydantic import BaseModel, EmailStr

# Sign Up
class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


# Sign In
class SignInRequest(BaseModel):
    email: EmailStr
    password: str

class SignInResponse(BaseModel):
    access_token: str
    id: str
    email: EmailStr
    name: str
    role: str