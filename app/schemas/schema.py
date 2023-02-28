from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    name: str
    password: str
    email: EmailStr

    class Config:
        orm_mode = True


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class SignUpRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    re_password: str


class UserUpdateRequest(BaseModel):
    name: Optional[str]
    password: Optional[str]


class UsersListResponse(BaseModel):
    users: list[User]
    total: int