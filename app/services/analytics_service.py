from databases                  import Database
from fastapi                    import HTTPException, status
from models.models              import Companies, Members, Statistics, Quizzes, Users
from schemas.analytics_schema   import *
from schemas.user_schema        import UserResponse
from sqlalchemy                 import select, insert, delete, update, desc


class AnalyticsService:

    def __init__(self, db:Database, user: UserResponse = None):
        self.db = db
        self.user = user

    
    async def attributes_check(self, user_id:int=None, quiz_id:int=None, company_id:int=None, permission:bool=False) -> None:
        if company_id:
            if not await self.db.fetch_one(query=select(Companies).where(Companies.company_id==company_id)):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This company not found")
        if permission:
            query = select(Members).where(Members.company_id==company_id, Members.user_id==self.user.result.user_id).filter(Members.role.in_(["owner", "admin"]))
            if not await self.db.fetch_one(query=query):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't have permission for this")
        if user_id:
            if not await self.db.fetch_one(query=select(Users).where(Users.user_id==user_id)):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user not found")
            if company_id:
                if not await self.db.fetch_one(query=select(Members).where(Members.company_id==company_id, Members.user_id==user_id)):
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This user not a member of this company")
        if quiz_id:
            quiz = await self.db.fetch_one(query=select(Quizzes).where(Quizzes.quiz_id == quiz_id))
            if not quiz:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This quiz not found")
            if company_id:
                 if quiz.company_id != company_id:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This quiz not in this company")


    async def rating_get_user(self, user_id:int) -> FloatResponse:
        await self.attributes_check(user_id=user_id)
        rating = await self.db.fetch_one(query=select(Statistics).where(Statistics.user_id == user_id).order_by(desc(Statistics.statistic_id)).limit(1))  
        if rating:
            return FloatResponse(detail="success", result=rating.all_average)
        return FloatResponse(detail="success", result=0.0)
    

    async def rating_get_company(self, user_id:int, company_id:int) -> FloatResponse:
        await self.attributes_check(user_id=user_id, company_id=company_id)
        rating = await self.db.fetch_one(query=select(Statistics).where(Statistics.user_id == user_id, Statistics.company_id==company_id).order_by(desc(Statistics.statistic_id)).limit(1))  
        if rating:
            return FloatResponse(detail="success", result=rating.company_average)
        return FloatResponse(detail="success", result=0.0)


    async def average_get_my_quizzes(self, quiz_id:int=None, company_id:int=None) -> QuizAttemptsResponse:
        await self.attributes_check(user_id=self.user.result.user_id, quiz_id=quiz_id, company_id=company_id)
        result=[]
        if quiz_id:
            attempts = await self.db.fetch_all(query=select(Statistics).where(Statistics.quiz_id==quiz_id, Statistics.user_id==self.user.result.user_id))
            result.append(QuizAttempts(quiz_id=quiz_id, result=[Attempt(**item) for item in attempts]))
        else:
            if company_id:
                companies = await self.db.fetch_all(query=select(Members).where(Members.company_id==company_id, Members.user_id == self.user.result.user_id))
            else:
                companies = await self.db.fetch_all(query=select(Members).where(Members.user_id == self.user.result.user_id))
            for company in companies:
                quizzes = await self.db.fetch_all(query=select(Quizzes).where(Quizzes.company_id==company.company_id))
                for quiz in quizzes:
                    attempts = await self.db.fetch_all(query=select(Statistics).where(Statistics.quiz_id==quiz.quiz_id, Statistics.user_id==self.user.result.user_id))
                    result.append(QuizAttempts(quiz_id=quiz.quiz_id, result=[Attempt(**item) for item in attempts]))
        return QuizAttemptsResponse(detail="success", result=result)
    

    async def datas_get_my(self) -> LastAttempts:
        quizzes = set(item.quiz_id for item in await self.db.fetch_all(query=select(Statistics).where(Statistics.user_id==self.user.result.user_id)))
        result = []
        for quiz_id in quizzes:
            last = await self.db.fetch_one(query=select(Statistics).where(Statistics.quiz_id==quiz_id, Statistics.user_id==self.user.result.user_id).order_by(desc(Statistics.statistic_id)).limit(1))
            result.append(LastAttempt(**last))
        return LastAttempts(detail="success", result=result)  


    async def average_get_company_quizzes(self, company_id:int) -> UserAttemptsResponse:
        await self.attributes_check(company_id=company_id, permission=True)
        result = []
        members = await self.db.fetch_all(query=select(Members).where(Members.company_id==company_id))
        for member in members:
            attempts = await self.db.fetch_all(query=select(Statistics).where(Statistics.user_id==member.user_id, Statistics.company_id==member.company_id))
            result.append(UserAttempt(user_id = member.user_id, result=[CompanyAttempt(**item) for item in attempts]))
        return UserAttemptsResponse(detail="success", result=result)
    

    async def average_get_company_quizzes_id(self, company_id:int, user_id:int=None) -> UserQuizAttemptsResponse:
        await self.attributes_check(company_id=company_id, user_id=user_id, permission=True)
        result = []
        attempts = await self.db.fetch_all(query=select(Statistics).where(Statistics.user_id==user_id, Statistics.company_id==company_id))
        result.append(UserQuizAttempt(user_id = user_id, result=[CompanyQuizAttempt(**item) for item in attempts]))
        return UserQuizAttemptsResponse(detail="success", result=result)
    

    async def average_get_company_quizzes_user_id(self, company_id:int, quiz_id:int=None) -> UserQuizAttemptsResponse:
        await self.attributes_check(company_id=company_id, quiz_id=quiz_id, permission=True)
        result = []
        members = await self.db.fetch_all(query=select(Members).where(Members.company_id==company_id))
        for member in members:
            attempts = await self.db.fetch_all(query=select(Statistics).where(Statistics.user_id==member.user_id, Statistics.company_id==company_id, Statistics.quiz_id==quiz_id))
            result.append(UserQuizAttempt(user_id = member.user_id, result=[CompanyQuizAttempt(**item) for item in attempts]))
        return UserQuizAttemptsResponse(detail="success", result=result)


    async def rating_get_company_owner(self, company_id:int, user_id:int=None) -> ManyFloatResponse:
        await self.attributes_check(user_id=user_id, company_id=company_id, permission=True)
        result = []
        if user_id:
            rating = await self.db.fetch_one(query=select(Statistics).where(Statistics.user_id == user_id).order_by(desc(Statistics.statistic_id)).limit(1))  
            if rating:
                return ManyFloatResponse(detail="success", result=[CompanyRating(**rating)])
            else:
                return ManyFloatResponse(detail="success", result=[CompanyRating(user_id=user_id, company_average=0.0)])
        members = await self.db.fetch_all(query=select(Members).where(Members.company_id==company_id))
        for member in members:
            rating = await self.db.fetch_one(query=select(Statistics).where(Statistics.user_id == member.user_id).order_by(desc(Statistics.statistic_id)).limit(1))
            if rating:
                result.append(CompanyRating(**rating))
            else:
                result.append(CompanyRating(user_id=member.user_id, company_average=0.0))
        return ManyFloatResponse(detail="success", result=result)


    async def datas_get_company(self, company_id:int) -> MemberLastsResponse:
        await self.attributes_check(company_id=company_id, permission=True)
        members = await self.db.fetch_all(query=select(Members).where(Members.company_id==company_id))
        result = []
        for member in members:
            last = await self.db.fetch_one(query=select(Statistics).where(Statistics.user_id==member.user_id, Statistics.company_id==company_id).order_by(desc(Statistics.statistic_id)).limit(1))
            if last:
                result.append(MemberLast(**last))
            else:
                result.append(MemberLast(user_id=member.user_id, quiz_passed_at=None))
        return MemberLastsResponse(detail="success", result=result)
    