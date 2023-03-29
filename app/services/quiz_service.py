from aioredis.client            import Redis
from databases                  import Database
from datetime                   import date, timedelta
from fastapi                    import HTTPException, status
from models.models              import Quizzes, Companies, Members, Questions, Statistics
from schemas.user_schema        import UserResponse
from schemas.quiz_schema        import *
from sqlalchemy                 import select, insert, delete, update, desc


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
        query = select(Quizzes).where(Quizzes.company_id == self.company_id)
        quizzes = await self.db.fetch_all(query=query)
        for quiz in quizzes:
            quiz.questions = await self.quiz_questions(quiz=quiz)
        quizzes = [Quiz(quiz_name=item.quiz_name, quiz_frequency=item.quiz_frequency, questions=item.questions, quiz_id=item.quiz_id, company_id=self.company_id) for item in quizzes]
        return QuizListResponse(detail="success", result = QuizList(quizzes=quizzes))


    async def quiz_get_id(self, quiz_id:int) -> QuizResponse:
        query = select(Quizzes).where(Quizzes.quiz_id == quiz_id)
        quiz = await self.db.fetch_one(query=query)
        if not quiz:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This quiz not found")
        self.company_id = quiz.company_id
        await self.member_check()
        quiz.questions = await self.quiz_questions(quiz=quiz)
        return QuizResponse(detail="success", result = Quiz(quiz_name=quiz.quiz_name, quiz_frequency = quiz.quiz_frequency, questions = quiz.questions, quiz_id=quiz.quiz_id, company_id=quiz.company_id))

    
    async def permission_check(self) -> None:
        await self.company_check()
        query = select(Members).where(Members.company_id==self.company_id, Members.user_id==self.user.result.user_id).filter(Members.role.in_(["owner", "admin"]))
        if not await self.db.fetch_one(query=query):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't have permission for this")


    async def quiz_delete(self, quiz_id:int) -> Response:
        result = await self.quiz_get_id(quiz_id=quiz_id)
        self.company_id = result.result.company_id
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
                                        company_id = self.company_id
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
        self.company_id = quiz.result.company_id
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
    

    async def quiz_passing(self, quiz_id:int, data: AnswerCreateRequest, redis: Redis) -> SubmitResponse:
        quiz = await self.quiz_get_id(quiz_id=quiz_id)
        self.company_id = quiz.result.company_id
        await self.member_check()
        quiz_statistics = await self.db.fetch_all(select(Statistics).where(Statistics.quiz_id == quiz_id, Statistics.user_id == self.user.result.user_id))
        attempt = len(quiz_statistics) + 1
        today = date.today()
        
        if quiz_statistics:
            quiz_statistics = quiz_statistics[-1]
            next_time = quiz_statistics.quiz_passed_at + timedelta(days=quiz.result.quiz_frequency) 
            if next_time > today:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"This user must wait until {next_time}")
        
        questions = await self.db.fetch_all(query=select(Questions).where(Questions.quiz_id==quiz_id))
        right = 0

        key = f"company_{self.company_id}:user_{self.user.result.user_id}:quiz_{quiz_id}:attempt_{attempt}"
        answers = {answer.question_id:answer.answer for answer in data.answers} if data.answers else {}
        
        for count, question in enumerate(questions):
            try:
                truth = question.question_right == answers[question.question_id]
                right += truth
                await redis.setex(key + f":question_{count+1}", 172800, f"Question '{question.question_name}': {answers[question.question_id]} is {'Right answer' if truth else 'Wrong answer'}")
            except KeyError:
                await redis.setex(key + f":question_{count+1}", 172800, f"Question '{question.question_name}': EMPTY ANSWER is 'Wrong answer'")

        company_statistics = await self.db.fetch_one(select(Statistics).where(Statistics.company_id == self.company_id, Statistics.user_id == self.user.result.user_id).order_by(desc(Statistics.statistic_id)).limit(1))
        all_statistics = await self.db.fetch_one(select(Statistics).where(Statistics.user_id == self.user.result.user_id).order_by(desc(Statistics.statistic_id)).limit(1))  
        quiz_questions = len(questions)
        quiz_right_answers = right
        quiz_average = quiz_right_answers / quiz_questions
        
        if quiz_statistics:
            quizzes_questions = quiz_statistics.quizzes_questions + quiz_questions
            quizzes_right_answers = quiz_statistics.quizzes_right_answers + quiz_right_answers
            quizzes_average = quizzes_right_answers / quizzes_questions
        else:
            quizzes_questions = quiz_questions
            quizzes_right_answers = quiz_right_answers
            quizzes_average = quiz_average
        
        if company_statistics:
            company_questions = company_statistics.company_questions + quiz_questions
            company_right_answers = company_statistics.company_right_answers + quiz_right_answers
            company_average = company_right_answers / company_questions
        else:
            company_questions = quiz_questions
            company_right_answers = quiz_right_answers
            company_average = quiz_average
        
        if all_statistics:
            all_questions = all_statistics.all_questions + quiz_questions
            all_right_answers = all_statistics.all_right_answers + quiz_right_answers
            all_average = all_right_answers / all_questions
        else:
            all_questions = quiz_questions
            all_right_answers = quiz_right_answers
            all_average = quiz_average
        
        await self.db.execute(query=insert(Statistics).values(
                                    company_id=self.company_id,
                                    user_id = self.user.result.user_id,
                                    quiz_id = quiz_id,
                                    quiz_questions = quiz_questions,
                                    quiz_right_answers = quiz_right_answers,
                                    quiz_average = quiz_average,
                                    quizzes_questions = quizzes_questions,
                                    quizzes_right_answers = quizzes_right_answers,
                                    quizzes_average = quizzes_average,
                                    company_questions = company_questions,
                                    company_right_answers = company_right_answers,
                                    company_average = company_average,
                                    all_questions = all_questions,
                                    all_right_answers = all_right_answers,
                                    all_average = all_average,
                                    quiz_passed_at = today))
        return SubmitResponse(detail="success", result=Submit(all_questions=quiz_questions, right_answers=quiz_right_answers, average=quiz_average))