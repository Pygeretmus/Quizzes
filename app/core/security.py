import datetime
import jwt
from decouple import config


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