from core.connections import get_db
from services.user_service import UserService 
from databases import Database
from schemas.user_schema import *
from fastapi import APIRouter, Depends, HTTPException, status
from core.security import create_access_token, decode_access_token
from fastapi.security import HTTPBearer
from routers.user_route import UserService
import random


router = APIRouter()

auth_token_schema = HTTPBearer()

async def get_current_user(token: str = Depends(auth_token_schema), db: Database = Depends(get_db)) -> UserResponse:
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not valid")
    try:
        email = payload["https://example.com/email"]
    except KeyError:
        email = payload["sub"]
        if not email:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email is not valid")
    user = await UserService(db=db).get_user_email(email=email)
    if not user:
        password = ''
        for x in range(10):
            password += random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))
        user = await UserService(db=db).create_user(account= SignUpRequest(
            user_email = email, 
            user_password = password,
            user_password_repeat = password,
            user_name = "User" 
        ))
    return user

@router.post('/login', response_model=TokenResponse)
async def autentification(login: SignInRequest, db: Database =Depends(get_db)) -> TokenResponse:
    await UserService(db=db).sign_in_verify(login=login)
    return TokenResponse(result = Token(access_token=create_access_token({'sub': login.user_email}), token_type="Bearer"))


@router.get('/me', response_model=UserResponse)
async def information(user: UserResponse = Depends(get_current_user)) -> UserResponse:
    return user
