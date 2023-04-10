import datetime, jwt

from core.connections       import get_db
from databases              import Database
from decouple               import config
from fastapi                import Depends, HTTPException, status
from fastapi.security       import HTTPBearer
from schemas.user_schema    import UserResponse
from services.user_service  import UserService


auth_token_schema = HTTPBearer()


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int))})
    return jwt.encode(to_encode, config("SECRET_KEY"), algorithm=config("ALGORITHM"))


def decode_access_token(token: str) -> dict:
    try:
        decoded_jwt = jwt.decode(jwt=token, key=(config("SECRET_KEY")), algorithms=config("ALGORITHM"), audience=config("AUDIENCE"), issuer=config("ISSUER"))
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Need to sign in")
    except jwt.exceptions.DecodeError:
        return None
    except jwt.exceptions.MissingRequiredClaimError:
        decoded_jwt = jwt.decode(jwt=token, key=config("SECRET_KEY"), algorithms=config("ALGORITHM"))
    

    return decoded_jwt


async def get_current_user(token: str = Depends(auth_token_schema), db: Database = Depends(get_db)) -> UserResponse:
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect token")
    try:
        user_email = payload["email"]
    except KeyError:
        user_email = payload["sub"]
        if not user_email:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email is not valid")
    return await UserService(db=db).current_user(user_email=user_email)