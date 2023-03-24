from pydantic               import BaseModel
from typing                 import Optional


class QuestionCreateRequest(BaseModel):
    question_name: str | None
    question_answers: list[str]
    question_right: str | None


class Question(QuestionCreateRequest):
    question_id: int


class QuestionUpdate(BaseModel):
    question_name: Optional[str] = None
    question_answers: Optional[list[str]] = None
    question_right: Optional[str] = None


class QuizCreateRequest(BaseModel):
    quiz_name: str | None
    quiz_frequency: int = 0
    questions: list[QuestionCreateRequest]


class Quiz(QuizCreateRequest):
    quiz_id: int
    questions: list[Question]
    quiz_company: int


class QuizList(BaseModel):
    quizzes: list[Quiz]     


class QuizUpdateRequest(BaseModel):
    quiz_name: Optional[str] = None
    quiz_frequency: Optional[int] = None
    questions: Optional[list[QuestionUpdate]] = None

class Response(BaseModel):
    detail: str


class QuizResponse(Response):
    result: Quiz


class QuizListResponse(Response):
    result: QuizList