from pydantic import BaseModel, EmailStr


# Sign Up
class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = "password"
    name: str


# Sign In
class SignInRequest(BaseModel):
    email: EmailStr
    password: str = "password"


class SignInResponse(BaseModel):
    access_token: str
    id: str
    email: EmailStr
    name: str
    role: str


# Phone
class UpdatePhoneRequest(BaseModel):
    phone: str


class SendPhoneOtpRequest(BaseModel):
    phone: str


class VerifyPhoneOtpRequest(BaseModel):
    phone: str
    token: str
