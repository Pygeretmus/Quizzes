import datetime, random

from argon2                 import PasswordHasher
from argon2.exceptions      import VerifyMismatchError
from databases              import Database
from fastapi                import HTTPException, status
from models.models          import Users, Members
from schemas.user_schema    import *
from sqlalchemy             import select, insert, delete, update




class UserService:

    def __init__(self, db:Database, user:UserResponse=None):
        self.db = db
        self.user = user


    async def user_get_all(self) -> UserListResponse:
        result = await self.db.fetch_all(query=select(Users))
        return UserListResponse(detail="success", result = UserList(users = [User(**item) for item in result]))


    async def user_get_id(self, user_id: int) -> UserResponse:
        query = select(Users).where(Users.user_id == user_id)
        result = await self.db.fetch_one(query=query)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user not found")
        return UserResponse(detail="success", result = User(**result))


    async def id_check(self, user_id: int) -> None:
        if self.user.result.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your account")


    async def user_delete(self, user_id: int) -> Response:
        await self.id_check(user_id=user_id)
        query = delete(Users).where(Users.user_id == user_id)
        await self.db.execute(query=query)
        return Response(detail="success")


    async def password_check(self, password: str) -> None:
        if not password:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Password required")
        elif len(password) < 4:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Password must be longer than three characters")


    async def user_get_email(self, user_email: str) -> UserResponse:
        query = select(Users).where(Users.user_email == user_email)
        result = await self.db.fetch_one(query=query)
        if result == None:
            return None
        return UserResponse(detail="success", result = User(**result))


    async def user_create(self, data: SignUpRequest) -> UserResponse:
        await self.password_check(data.user_password)
        if await self.user_get_email(user_email = data.user_email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        if data.user_password != data.user_password_repeat:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Password and Confirm Password must be match")
        if not bool(data.user_name):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Name required")
        hashed_password = PasswordHasher().hash(data.user_password)
        query = insert(Users).values(
            user_email = data.user_email,
            user_password = hashed_password,
            user_name = data.user_name,
            user_registred_at = datetime.datetime.utcnow()
        ).returning(Users)
        return UserResponse(detail="success", result=await self.db.fetch_one(query=query))


    async def make_changes(self, data: UserUpdateRequest) -> UserUpdateRequest:
        result = {}
        for items in data:
            if items[1]:
                result[items[0]] = items[1]
        return result


    async def user_update(self, user_id: int, data: UserUpdateRequest) -> UserResponse: 
        await self.id_check(user_id=user_id)
        changes = await self.make_changes(data = data)
        if changes: 
            if "user_password" in changes.keys():
                await self.password_check(changes["user_password"])
                changes["user_password"] = PasswordHasher().hash(changes["user_password"])
            query = update(Users).where(Users.user_id == user_id).values(dict(changes))
            await self.db.execute(query=query)
        return await self.user_get_id(user_id=user_id)


    async def current_user(self, user_email: str) -> UserResponse:
        user = await self.user_get_email(user_email=user_email)
        if not user:
            password = ''
            for x in range(10):
                password += random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))
            user = await self.user_create(data= SignUpRequest(
                user_email = user_email, 
                user_password = password,
                user_password_repeat = password,
                user_name = "User" 
        ))
        return user
    
    
    async def sign_in_verify(self, login: SignInRequest) -> None:
        await self.password_check(password=login.user_password)
        query = select(Users).where(Users.user_email == login.user_email)
        result = await self.db.fetch_one(query=query)
        if result == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user not found")
        try:
            PasswordHasher().verify(hash=result.user_password, password=login.user_password)
        except VerifyMismatchError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    
    async def company_leave(self, company_id:int) -> Response:
        query = delete(Members).where(Members.company_id==company_id, Members.user_id == self.user.result.user_id)
        await self.db.execute(query=query)
        return Response(detail="success")