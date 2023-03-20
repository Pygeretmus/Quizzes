from core.connections       import get_db
from core.security          import get_current_user
from databases              import Database
from fastapi                import APIRouter, Depends
from schemas.user_schema    import *
from services.user_service  import UserService 


router = APIRouter()


@router.get('/users/', response_model=UserListResponse)
async def get_all_users(user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> UserListResponse:
    return await UserService(db=db).user_get_all()
 

@router.get('/user/{user_id}/', response_model=UserResponse)
async def get_user_by_id(user_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> UserResponse:
    return await UserService(db=db).user_get_id(user_id=user_id)


@router.delete('/user/{user_id}/', response_model=Response)
async def user_delete_id(user_id: int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> Response:
    return await UserService(db=db, user=user).user_delete(user_id=user_id)


@router.post('/user/', response_model=UserResponse)
async def create_new_user(data:SignUpRequest, db: Database = Depends(get_db)) -> UserResponse:
    return await UserService(db=db).user_create(data=data)


@router.put('/user/{user_id}/', response_model=UserResponse)
async def upgrade_user(user_id: int, data:UserUpdateRequest, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> UserResponse:
    return await UserService(db=db, user=user).user_update(user_id=user_id, data=data)


@router.delete("/company/{company_id}/leave/", response_model=Response)
async def leave_company(company_id: int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> Response:
    return await UserService(db=db, user=user).company_leave(company_id=company_id)