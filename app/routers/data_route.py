from aioredis.client        import Redis
from core.connections       import get_db, get_redis
from core.security          import get_current_user
from databases              import Database
from fastapi                import APIRouter, Depends
from starlette.responses    import StreamingResponse
from schemas.quiz_schema    import DataListResponse
from schemas.user_schema    import UserResponse
from services.data_service  import DataService


router = APIRouter()


@router.get('/my/', response_model=DataListResponse)
async def get_data_me(user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db), redis: Redis=Depends(get_redis)) -> DataListResponse:
    return await DataService(db=db, redis=redis, user=user).data_me()
 

@router.get('/my/csv', response_class=StreamingResponse)
async def get_data_me_csv(user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db), redis: Redis=Depends(get_redis)) -> StreamingResponse:
    return await DataService(db=db, redis=redis, user=user).data_me(file=True)


@router.get('/my/company/{company_id}/', response_model=DataListResponse)
async def get_data_me_company(company_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db), redis: Redis=Depends(get_redis)) -> DataListResponse:
    return await DataService(db=db, redis=redis, user=user).data_me(company_id=company_id)


@router.get('/my/company/{company_id}/csv/', response_class=StreamingResponse)
async def get_data_me_company_csv(company_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db), redis: Redis=Depends(get_redis)) -> StreamingResponse:
    return await DataService(db=db, redis=redis, user=user).data_me(company_id=company_id, file=True)


@router.get('/my/quiz/{quiz_id}/', response_model=DataListResponse)
async def get_data_me_quiz(quiz_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db), redis: Redis=Depends(get_redis)) -> DataListResponse:
    return await DataService(db=db, redis=redis, user=user).data_me(quiz_id=quiz_id)


@router.get('/my/quiz/{quiz_id}/csv/', response_class=StreamingResponse)
async def get_data_me_quiz_csv(quiz_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db), redis: Redis=Depends(get_redis)) -> StreamingResponse:
    return await DataService(db=db, redis=redis, user=user).data_me(quiz_id=quiz_id, file=True)


@router.get('/company/{company_id}/', response_model=DataListResponse)
async def get_data_company(company_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db), redis: Redis=Depends(get_redis)) -> DataListResponse:
    return await DataService(db=db, redis=redis, user=user, company_id=company_id).data_company()


@router.get('/company/{company_id}/csv/', response_class=StreamingResponse)
async def get_data_company_csv(company_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db), redis: Redis=Depends(get_redis)) -> StreamingResponse:
    return await DataService(db=db, redis=redis, user=user, company_id=company_id).data_company(file=True)


@router.get('/company/{company_id}/quiz/{quiz_id}/', response_model=DataListResponse)
async def get_data_company_quiz(company_id:int, quiz_id: int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db), redis: Redis=Depends(get_redis)) -> DataListResponse:
    return await DataService(db=db, redis=redis, user=user, company_id=company_id).data_company(quiz_id=quiz_id)


@router.get('/company/{company_id}/quiz/{quiz_id}/csv/', response_class=StreamingResponse)
async def get_data_company_quiz_csv(company_id:int, quiz_id: int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db), redis: Redis=Depends(get_redis)) -> StreamingResponse:
    return await DataService(db=db, redis=redis, user=user, company_id=company_id).data_company(quiz_id=quiz_id, file=True)


@router.get('/company/{company_id}/user/{user_id}/', response_model=DataListResponse)
async def get_data_company_quiz(company_id:int, user_id: int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db), redis: Redis=Depends(get_redis)) -> DataListResponse:
    return await DataService(db=db, redis=redis, user=user, company_id=company_id).data_company(user_id=user_id)


@router.get('/company/{company_id}/user/{user_id}/csv/', response_class=StreamingResponse)
async def get_data_company_quiz_csv(company_id:int, user_id: int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db), redis: Redis=Depends(get_redis)) -> StreamingResponse:
    return await DataService(db=db, redis=redis, user=user, company_id=company_id).data_company(user_id=user_id, file=True)


@router.get('/company/{company_id}/quiz/{quiz_id}/user/{user_id}/', response_model=DataListResponse)
async def get_data_company_quiz_user(company_id:int, quiz_id: int, user_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db), redis: Redis=Depends(get_redis)) -> DataListResponse:
    return await DataService(db=db, redis=redis, user=user, company_id=company_id).data_company(quiz_id=quiz_id, user_id=user_id)


@router.get('/company/{company_id}/quiz/{quiz_id}/user/{user_id}/csv/', response_class=StreamingResponse)
async def get_data_company_quiz_user_csv(company_id:int, quiz_id: int, user_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db), redis: Redis=Depends(get_redis)) -> StreamingResponse:
    return await DataService(db=db, redis=redis, user=user, company_id=company_id).data_company(quiz_id=quiz_id, user_id=user_id, file=True)


