from databases import Database
from models.models import Users
from schemas.user_schema import *
from sqlalchemy import select, insert, delete, update
from argon2 import PasswordHasher
from fastapi import HTTPException


async def password_check(password: str):
    if not password:
        raise HTTPException(status_code=422, detail="Password not specified")
    elif len(password) < 4:
        raise HTTPException(status_code=422, detail="Password must be longer than three characters")


async def get_users(db: Database) -> UserListResponse:
    query = select(Users)
    result = await db.fetch_all(query=query)
    return UserListResponse(result = Userlist(users = [User(**item) for item in result]))


async def get_user_id(db: Database, id: int) -> UserResponse:
    query = select(Users).where(Users.user_id == id)
    result = await db.fetch_one(query=query)
    if not result:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    return UserResponse(result = User(**result))


async def create_user(db: Database, account: SignUpRequest) -> UserResponse:
    await password_check(account.user_password)
    query = select(Users).where(Users.user_email == account.user_email)
    result = await db.fetch_one(query=query)
    if result:
        raise HTTPException(status_code=400, detail="Email already exist")
    if account.user_password != account.user_password_repeat:
        raise HTTPException(status_code=422, detail="Invalid repeat password")
    hashed_password = PasswordHasher().hash(account.user_password)
    query = insert(Users).values({
        "user_email" : account.user_email,
        "user_password" : hashed_password,
        "user_name" : account.user_name}
    ).returning(Users)
    id = await db.execute(query=query)
    return await get_user_id(db=db, id=id)


async def delete_user(db: Database, id: int) -> str:
    await get_user_id(db=db, id=id)
    query = delete(Users).where(Users.user_id == id)
    await db.execute(query=query)
    return "Successfully deleted"


async def update_user(db: Database, id: int, changes: UserUpdateRequest):
    await get_user_id(db=db, id=id)
    if changes: 
        if "user_password" in changes.keys():
            await password_check(changes["user_password"])
            changes["user_password"] = PasswordHasher().hash(changes["user_password"])
        query = update(Users).where(Users.user_id == id).values(dict(changes)).returning(Users)
        id = await db.execute(query=query)
    return await get_user_id(db=db, id=id)