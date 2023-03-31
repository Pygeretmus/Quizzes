from pydantic               import BaseModel
from datetime               import date


class Response(BaseModel):
    detail: str


class FloatResponse(Response):
    result: float


class CompanyRating(BaseModel):
    user_id: int
    company_average: float


class ManyFloatResponse(Response):
    result: list[CompanyRating]


class Attempt(BaseModel):
    quiz_passed_at: date
    quiz_average: float
    quizzes_average: float


class QuizAttempts(BaseModel):
    quiz_id:int
    result:list[Attempt]
    

class QuizAttemptsResponse(Response):
    result: list[QuizAttempts]


class LastAttempt(BaseModel):
    quiz_passed_at: date
    quiz_id: int


class LastAttempts(Response):
    result: list[LastAttempt]


class CompanyAttempt(BaseModel):
    quiz_id: int
    quiz_passed_at: date
    company_average: float


class CompanyQuizAttempt(BaseModel):
    quiz_id: int
    quiz_passed_at: date
    quiz_average: float
    quizzes_average: float


class UserAttempt(BaseModel):
    user_id:int
    result:list[CompanyAttempt]


class UserQuizAttempt(BaseModel):
    user_id:int
    result:list[CompanyQuizAttempt]


class UserQuizAttemptsResponse(Response):
    result: list[UserQuizAttempt]


class UserAttemptsResponse(Response):
    result: list[UserAttempt]


class MemberLast(BaseModel):
    user_id:int
    quiz_passed_at:date | None


class MemberLastsResponse(Response):
    result: list[MemberLast]