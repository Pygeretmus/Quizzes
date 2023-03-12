from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime


class User(BaseModel):
    user_id: int
    user_name: str
    user_email: EmailStr
    user_status: Optional[str]
    user_registred_at: datetime.datetime 

    class Config:
        orm_mode = True


class Userlist(BaseModel):
    users: list[User]


class Account(User):
    user_password: str


class SignInRequest(BaseModel):
    user_password: str
    user_email: EmailStr


class SignUpRequest(SignInRequest):
    user_password_repeat: str
    user_name: str


class UserUpdateRequest(BaseModel):
    user_name: Optional[str] = ""
    user_password: Optional[str] = ""


class UserResponse(BaseModel):
    result: User


class UserListResponse(BaseModel):
    result: Userlist


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenResponse(BaseModel):
    result: Token