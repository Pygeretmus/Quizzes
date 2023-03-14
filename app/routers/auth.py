from core.connections import get_db
from services.user_service import UserService 
from databases import Database
from schemas.user_schema import *
from fastapi import APIRouter, Depends
from core.security import create_access_token
from routers.user_route import UserService
from core.security import get_current_user


router = APIRouter()


@router.post('/login', response_model=TokenResponse)
async def autentification(login: SignInRequest, db: Database =Depends(get_db)) -> TokenResponse:
    await UserService(db=db).sign_in_verify(login=login)
    return TokenResponse(result = Token(access_token=create_access_token({'sub': login.user_email}), token_type="Bearer"))


@router.get('/me', response_model=UserResponse)
async def information(user: UserResponse = Depends(get_current_user)) -> UserResponse:
    return user

@router.get('/me', response_model=UserResponse)
async def information(user: UserResponse = Depends(get_current_user)) -> UserResponse:
    return user