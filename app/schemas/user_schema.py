from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    user_id: int
    user_name: str
    user_email: EmailStr
    
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