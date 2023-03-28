from core.connections       import get_db
from core.security          import get_current_user
from databases              import Database
from fastapi                import APIRouter, Depends
from schemas.user_schema    import UserResponse
from schemas.quiz_schema    import *
from services.quiz_service  import QuizService


router = APIRouter()


@router.get('/company/{company_id}/quizes', response_model=QuizListResponse)
async def get_all_quizzes(company_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> QuizListResponse:
    return await QuizService(db=db, company_id=company_id, user=user).quiz_get_all()
 

@router.get('/quiz/{quiz_id}/', response_model=QuizResponse)
async def get_quiz_by_id(quiz_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> QuizResponse:
    return await QuizService(db=db, user=user).quiz_get_id(quiz_id=quiz_id)


@router.delete('/quiz/{quiz_id}/', response_model=Response)
async def quiz_delete_id(quiz_id: int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> Response:
    return await QuizService(db=db, user=user).quiz_delete(quiz_id=quiz_id)


@router.post('/company/{company_id}/quiz/', response_model=QuizResponse)
async def create_new_quiz(data:QuizCreateRequest, company_id: int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> QuizResponse:
    return await QuizService(db=db, user=user, company_id=company_id).quiz_create(data=data)


@router.put('/quiz/{quiz_id}/', response_model=QuizResponse)
async def upgrade_quiz(quiz_id: int, data:QuizUpdateRequest, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> QuizResponse:
    return await QuizService(db=db, user=user).quiz_update(quiz_id=quiz_id, data=data)


@router.post('/attempt/{quiz_id}/', response_model=SubmitResponse)
async def passing_quiz(quiz_id: int, data:AnswerCreateRequest, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> SubmitResponse:
    return await QuizService(db=db, user=user).quiz_passing(quiz_id=quiz_id, data=data)