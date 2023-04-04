from core.connections           import get_db
from core.security              import get_current_user
from databases                  import Database
from fastapi                    import APIRouter, Depends
from schemas.analytics_schema   import *
from schemas.user_schema        import UserResponse
from services.analytics_service import AnalyticsService


router = APIRouter()


@router.get('/user/{user_id}/', response_model=FloatResponse)
async def get_user_rating(user_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> FloatResponse:
    return await AnalyticsService(db=db).rating_get_user(user_id=user_id)


@router.get('/my/', response_model=FloatResponse)
async def get_my_rating(user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> FloatResponse:
    return await AnalyticsService(db=db).rating_get_user(user_id=user.result.user_id)


@router.get('/my/company/{company_id}/', response_model=FloatResponse)
async def get_my_company_rating(company_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> FloatResponse:
    return await AnalyticsService(db=db).rating_get_company(user_id=user.result.user_id, company_id=company_id)


@router.get('/my/average/', response_model=QuizAttemptsResponse)
async def get_my_average(user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> QuizAttemptsResponse:
    return await AnalyticsService(db=db, user=user).average_get_my_quizzes()


@router.get('/my/average/company/{company_id}/', response_model=QuizAttemptsResponse)
async def get_my_average_company(company_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> QuizAttemptsResponse:
    return await AnalyticsService(db=db, user=user).average_get_my_quizzes(company_id=company_id)


@router.get('/my/average/quiz/{quiz_id}/', response_model=QuizAttemptsResponse)
async def get_my_average_quiz(quiz_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> QuizAttemptsResponse:
    return await AnalyticsService(db=db, user=user).average_get_my_quizzes(quiz_id=quiz_id)


@router.get('/my/datas/', response_model=LastAttempts)
async def get_my_last_attempts(user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> LastAttempts:
    return await AnalyticsService(db=db, user=user).datas_get_my()


@router.get('/company/{company_id}/average/', response_model=UserAttemptsResponse)
async def get_company_average(company_id:int,user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> UserAttemptsResponse:
    return await AnalyticsService(db=db, user=user).average_get_company_quizzes(company_id=company_id)


@router.get('/company/{company_id}/average/user/{user_id}/', response_model=UserQuizAttemptsResponse)
async def get_company_average_user(user_id:int, company_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> UserQuizAttemptsResponse:
    return await AnalyticsService(db=db, user=user).average_get_company_quizzes_id(company_id=company_id, user_id=user_id)


@router.get('/company/{company_id}/average/quiz/{quiz_id}/', response_model=UserQuizAttemptsResponse)
async def get_company_average_quiz(quiz_id:int, company_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> UserQuizAttemptsResponse:
    return await AnalyticsService(db=db, user=user).average_get_company_quizzes_user_id(company_id=company_id, quiz_id=quiz_id)


@router.get('/company/{company_id}/user/{user_id}/rating/', response_model=ManyFloatResponse)
async def get_user_company_rating(company_id:int, user_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> ManyFloatResponse:
    return await AnalyticsService(db=db, user=user).rating_get_company_owner(user_id=user_id, company_id=company_id)


@router.get('/company/{company_id}/rating/', response_model=ManyFloatResponse)
async def get_user_company_rating_all(company_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> ManyFloatResponse:
    return await AnalyticsService(db=db, user=user).rating_get_company_owner(company_id=company_id)


@router.get('/company/{company_id}/datas/', response_model=MemberLastsResponse)
async def get_company_last_attempts(company_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> MemberLastsResponse:
    return await AnalyticsService(db=db, user=user).datas_get_company(company_id=company_id)




