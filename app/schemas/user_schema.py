import datetime

from pydantic               import BaseModel, EmailStr
from typing                 import Optional


class User(BaseModel):
    user_id: int
    user_name: str
    user_email: EmailStr
    user_status: Optional[str]
    user_registred_at: datetime.datetime

    class Config:
        orm_mode = True


class UserList(BaseModel):
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
    user_name: Optional[str] = None
    user_password: Optional[str] = None


class UserResponse(BaseModel):
    result: User
    detail: str


class UserListResponse(BaseModel):
    result: UserList
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenResponse(BaseModel):
    result: Token
    detail: str