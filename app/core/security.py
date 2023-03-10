import datetime
from jose import jwt
from decouple import config



def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int))})
    return jwt.encode(to_encode, config("SECRET_KEY"), algorithm=config("ALGORITHM"))


def decode_access_token(token: str):
    try:
        encoded_jwt = jwt.decode(token, config('SECRET_KEY'), algorithms=config("ALGORITHM"))
    except jwt.JWSError and jwt.JWTError:
        return None
    return encoded_jwt