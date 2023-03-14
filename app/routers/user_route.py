from core.connections import get_db
from services.user_service import UserService 
from databases import Database
from schemas.user_schema import *
from fastapi import APIRouter, Depends
from core.security import get_current_user


router = APIRouter()


@router.get('/users', response_model=UserListResponse)
async def get_all_users(user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> UserListResponse:
    return await UserService(db=db).get_users()
 

@router.get('/user', response_model=UserResponse)
async def get_user_by_id(user_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> UserResponse:
    return await UserService(db=db).get_user_id(id=user_id)


@router.delete('/user', response_model=str)
async def delete_user_id(user_id: int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> str:
    return await UserService(db=db, user=user).delete_user(id=user_id)


@router.post('/user', response_model=UserResponse)
async def create_new_user(data:SignUpRequest, db: Database = Depends(get_db)) -> UserResponse:
    return await UserService(db=db).create_user(account=data)


@router.put('/user', response_model=UserResponse)
async def upgrade_user(user_id: int, data:UserUpdateRequest, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> UserResponse:
    return await UserService(db=db, user=user).update_user(id=user_id, data=data)


