from databases                  import Database
from fastapi                    import HTTPException, status
from models.models              import Quizzes, Companies, Members, Users, Questions
from schemas.user_schema        import UserResponse
from schemas.company_schema     import CompanyResponse, Company
from schemas.quiz_schema        import *
from sqlalchemy                 import select, insert, delete, update


class QuizService:

    def __init__(self, db:Database, company_id: int = None, user: UserResponse = None):
        self.db = db
        self.user = user
        self.company_id = company_id


    async def company_check(self) -> None:
        if not await self.db.fetch_one(query=select(Companies).where(Companies.company_id==self.company_id)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This company not found")


    async def member_check(self) -> None:
        await self.company_check()
        if not await self.db.fetch_one(query=select(Members).where(Members.company_id==self.company_id, Members.user_id==self.user.result.user_id)):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This user not a member of this company")


    async def quiz_questions(self, quiz) -> list[Question]:
        questions = await self.db.fetch_all(query= select(Questions).where(Questions.quiz_id == quiz.quiz_id))
        return [Question(**item) for item in questions]
    

    async def quiz_get_all(self) -> QuizListResponse:
        await self.member_check()
        query = select(Quizzes).where(Quizzes.quiz_company == self.company_id)
        quizzes = await self.db.fetch_all(query=query)
        for quiz in quizzes:
            quiz.questions = await self.quiz_questions(quiz=quiz)
        quizzes = [Quiz(quiz_name=item.quiz_name, quiz_frequency=item.quiz_frequency, questions=item.questions, quiz_id=item.quiz_id, quiz_company=self.company_id) for item in quizzes]
        return QuizListResponse(detail="success", result = QuizList(quizzes=quizzes))


    async def quiz_get_id(self, quiz_id:int) -> QuizResponse:
        query = select(Quizzes).where(Quizzes.quiz_id == quiz_id)
        quiz = await self.db.fetch_one(query=query)
        if not quiz:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This quiz not found")
        self.company_id = quiz.quiz_company
        await self.member_check()
        quiz.questions = await self.quiz_questions(quiz=quiz)
        return QuizResponse(detail="success", result = Quiz(quiz_name=quiz.quiz_name, quiz_frequency = quiz.quiz_frequency, questions = quiz.questions, quiz_id=quiz.quiz_id, quiz_company=quiz.quiz_company))

    
    async def permission_check(self) -> None:
        await self.company_check()
        query = select(Members).where(Members.company_id==self.company_id, Members.user_id==self.user.result.user_id).filter(Members.role.in_(["owner", "admin"]))
        if not await self.db.fetch_one(query=query):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't have permission for this")


    async def quiz_delete(self, quiz_id:int) -> Response:
        result = await self.quiz_get_id(quiz_id=quiz_id)
        self.company_id = result.result.quiz_company
        await self.permission_check()
        query = delete(Quizzes).where(Quizzes.quiz_id == quiz_id)
        await self.db.execute(query=query)
        return Response(detail="success")


    async def quiz_check(self, data: Quiz) -> None:
        if len(data.questions) < 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz must have more than one question")
        question_names = []
        for question in data.questions:
            if not bool(question.question_name):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Question name required")
            if len(question.question_answers) < 2:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Question must have more than one answer")
            if question.question_name in question_names:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Question must have unique name")
            question_names.append(question.question_name)
            answer_names = []
            for answer in question.question_answers:
                if not bool(answer):
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Answer name required")
                if answer in answer_names:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Answer must have unique name")
                answer_names.append(answer)
            if question.question_right not in question.question_answers:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Right answer not in the answers")


    async def quiz_create(self, data: Quiz) -> QuizResponse:
        await self.permission_check()
        if not bool(data.quiz_name):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz name required")
        await self.quiz_check(data=data)
        quiz_id = await self.db.execute(query = insert(Quizzes).values(
                                        quiz_name = data.quiz_name,
                                        quiz_frequency = data.quiz_frequency,
                                        quiz_company = self.company_id
                                        ).returning(Quizzes))
        values = []
        for question in data.questions:
            values += [{"question_name": question.question_name, "question_answers": question.question_answers, "question_right": question.question_right, "quiz_id": quiz_id}]
        await self.db.execute_many(query=insert(Questions), values=values)
        return await self.quiz_get_id(quiz_id=quiz_id)
    

    async def make_changes(self, data:QuizUpdateRequest) -> QuizUpdateRequest:
        result = {}
        for items in data:
            if items[1]:
                result[items[0]] = items[1]
        return result


    async def quiz_update(self, quiz_id:int, data: QuizUpdateRequest) -> QuizResponse:
        quiz = await self.quiz_get_id(quiz_id=quiz_id)
        self.company_id = quiz.result.quiz_company
        await self.permission_check()
        try:
            if data.questions:
                await self.quiz_check(data=data)
                await self.db.execute(query=delete(Questions).where(Questions.quiz_id==quiz_id))
                values = []
                for question in data.questions:
                    values += [{"question_name": question.question_name, "question_answers": question.question_answers, "question_right": question.question_right, "quiz_id": quiz_id}]
                await self.db.execute_many(query=insert(Questions), values=values)
                del data.questions
        except KeyError:
            pass
        data = await self.make_changes(data=data)
        if data:
            await self.db.execute(query=update(Quizzes).where(Quizzes.quiz_id == quiz_id).values(dict(data)))
            return await self.quiz_get_id(quiz_id=quiz_id)
        return await self.quiz_get_id(quiz_id=quiz_id)