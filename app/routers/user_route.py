from core.connections import get_db
from services import user_service
from databases import Database
from schemas.user_schema import *
from fastapi import APIRouter, Depends


router = APIRouter()


@router.get('/users', response_model=UserListResponse)
async def get_all_users(db: Database = Depends(get_db)) -> UserListResponse:
    return await user_service.get_users(db=db)
 

@router.get('/user', response_model=UserResponse)
async def get_user_by_id(user_id:int, db: Database = Depends(get_db)) -> UserResponse:
    return await user_service.get_user_id(db=db, id=user_id)


@router.delete('/user', response_model=str)
async def delete_user_id(user_id: int, db: Database = Depends(get_db)) -> str:
    return await user_service.delete_user(db=db, id=user_id)


@router.post('/user', response_model=UserResponse)
async def create_new_user(data:SignUpRequest, db: Database = Depends(get_db)) -> UserResponse:
    return await user_service.create_user(db=db, account=data)


@router.put('/user', response_model=UserResponse)
async def upgrade_user(user_id: int, data:UserUpdateRequest, db: Database = Depends(get_db)) -> UserResponse:
    changes = {item[0]: item[1] for item in data if item[1]}
    return await user_service.update_user(db=db, id=user_id, changes=changes)

