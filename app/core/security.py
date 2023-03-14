import datetime, random, jwt
from decouple import config
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from databases import Database
from core.connections import get_db
from schemas.user_schema import UserResponse, SignUpRequest
from services.user_service import UserService


auth_token_schema = HTTPBearer()


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int))})
    return jwt.encode(to_encode, config("SECRET_KEY"), algorithm=config("ALGORITHM"))


def decode_access_token(token: str) -> dict:
    try:
        decoded_jwt = jwt.decode(jwt=token, key=(config("SECRET_KEY")), algorithms=config("ALGORITHM"), audience=config("AUDIENCE"), issuer=config("ISSUER"))
    except jwt.exceptions.DecodeError:
        return None
    except jwt.exceptions.MissingRequiredClaimError:
        decoded_jwt = jwt.decode(jwt=token, key=config("SECRET_KEY"), algorithms=config("ALGORITHM"))
    return decoded_jwt


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