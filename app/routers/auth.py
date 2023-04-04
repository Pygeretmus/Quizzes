from core.connections       import get_db
from core.security          import create_access_token, get_current_user
from databases              import Database
from fastapi                import APIRouter, Depends
from routers.user_route     import UserService
from services.user_service  import UserService 
from schemas.user_schema    import *



router = APIRouter()


@router.post('/login/', response_model=TokenResponse)
async def autentification(login: SignInRequest, db: Database =Depends(get_db)) -> TokenResponse:
    await UserService(db=db).sign_in_verify(login=login)
    return TokenResponse(detail="success", result = Token(access_token=create_access_token({'sub': login.user_email}), token_type="Bearer"))


@router.get('/my/', response_model=UserResponse)
async def information(user: UserResponse = Depends(get_current_user)) -> UserResponse:
    return user