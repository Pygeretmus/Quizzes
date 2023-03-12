from core.connections import get_db
from services.user_service import UserService 
from databases import Database
from schemas.user_schema import *
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer


router = APIRouter()

auth_token_schema = HTTPBearer()


@router.get('/users', response_model=UserListResponse)
async def get_all_users(token: str = Depends(auth_token_schema), db: Database = Depends(get_db)) -> UserListResponse:
    return await UserService(db=db).get_users(token=token)
 

@router.get('/user', response_model=UserResponse)
async def get_user_by_id(user_id:int, token: str = Depends(auth_token_schema), db: Database = Depends(get_db)) -> UserResponse:
    return await UserService(db=db).get_user_id(id=user_id, token=token)


@router.delete('/user', response_model=str)
async def delete_user_id(user_id: int, token: str = Depends(auth_token_schema), db: Database = Depends(get_db)) -> str:
    return await UserService(db=db).delete_user(id=user_id, token=token)


@router.post('/user', response_model=UserResponse)
async def create_new_user(data:SignUpRequest, db: Database = Depends(get_db)) -> UserResponse:
    return await UserService(db=db).create_user(account=data)


@router.put('/user', response_model=UserResponse)
async def upgrade_user(user_id: int, data:UserUpdateRequest, token: str = Depends(auth_token_schema), db: Database = Depends(get_db)) -> UserResponse:
    return await UserService(db=db).update_user(id=user_id, data=data, token=token)


