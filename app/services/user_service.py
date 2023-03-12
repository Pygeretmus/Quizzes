from databases import Database
from models.models import Users
from schemas.user_schema import *
from sqlalchemy import select, insert, delete, update
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException, status
import datetime
import random
from core.security import create_access_token, decode_access_token
from pydantic import ValidationError


class UserService:

    def __init__(self, db:Database):
        self.db = db


    async def make_changes(self, data: UserUpdateRequest) -> UserUpdateRequest:
        result = {}
        for items in data:
            if items[1]:
                result[items[0]] = items[1]
        return result


    async def password_check(self, password: str):
        if not password:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Password not specified")
        elif len(password) < 4:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Password must be longer than three characters")


    async def get_user_email(self, email: str) -> UserResponse:
        query = select(Users).where(Users.user_email == email)
        result = await self.db.fetch_one(query=query)
        if result == None:
            return None
        return UserResponse(result = result)
    

    async def sign_in_verify(self, login: SignInRequest):
        query = select(Users).where(Users.user_email == login.user_email)
        result = await self.db.fetch_one(query=query)
        if result == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist")
        try:
            PasswordHasher().verify(hash=result.user_password, password=login.user_password)
        except VerifyMismatchError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")


    async def validate(self, token: str):
        payload = decode_access_token(token.credentials)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not valid")
        try:
            email = payload["https://example.com/email"]
        except KeyError:
            email = payload["sub"]
            if not email:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email is not valid")
        user = await self.get_user_email(email=email)
        if not user:
            password = ''
            for x in range(10):
                password += random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))
            user = await self.create_user(account= SignUpRequest(
            user_email = email, 
            user_password = password,
            user_password_repeat = password,
            user_name = "User" 
        ))
        return user


    async def get_users(self, token:str) -> UserListResponse:
        await self.validate(token=token)
        query = select(Users)
        result = await self.db.fetch_all(query=query)
        return UserListResponse(result = Userlist(users = [User(**item) for item in result]))


    async def get_user_id(self, id: int, token: str) -> UserResponse:
        await self.validate(token=token)
        query = select(Users).where(Users.user_id == id)
        result = await self.db.fetch_one(query=query)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist")
        return UserResponse(result = User(**result))
    

    async def create_user(self, account: SignUpRequest) -> UserResponse:
        await self.password_check(account.user_password)
        if await self.get_user_email(email = account.user_email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist")
        if account.user_password != account.user_password_repeat:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid repeat password")
        hashed_password = PasswordHasher().hash(account.user_password)
        query = insert(Users).values(
            user_email = account.user_email,
            user_password = hashed_password,
            user_name = account.user_name,
            user_registred_at = datetime.datetime.utcnow()
        ).returning(Users)
        return UserResponse(result=await self.db.fetch_one(query=query))


    async def delete_user(self, id: int, token:str) -> str:
        user = await self.validate(token=token) 
        if user.result.user_id != id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your account")
        query = delete(Users).where(Users.user_id == id)
        await self.db.execute(query=query)
        return "Successfully deleted"


    async def update_user(self, id: int, data: UserUpdateRequest, token:str) -> UserResponse:
        user = await self.validate(token=token) 
        if user.result.user_id != id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your account")
        changes = await self.make_changes(data = data)
        if changes: 
            if "user_password" in changes.keys():
                await self.password_check(changes["user_password"])
                changes["user_password"] = PasswordHasher().hash(changes["user_password"])
            query = update(Users).where(Users.user_id == id).values(dict(changes)).returning(Users)
        return UserResponse(result=await self.db.fetch_one(query=query))