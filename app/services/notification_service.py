from databases                          import Database
from datetime                           import date, timedelta, datetime
from fastapi                            import HTTPException, status
from models.models                      import Notifications, Quizzes, Members, Statistics, Companies
from schemas.user_schema                import UserResponse
from schemas.notification_schema        import *
from sqlalchemy                         import select, delete, update, desc, insert


class NotificationService:

    def __init__(self, db:Database, user: UserResponse = None):
        self.db = db
        self.user = user

    
    async def notification_get(self, read:bool=None) -> NotificationResponse:
        if read == None:
            notifications = await self.db.fetch_all(query=select(Notifications).where(Notifications.user_id==self.user.result.user_id).order_by(desc(Notifications.notification_id)))
        else:
            notifications = await self.db.fetch_all(query=select(Notifications).where(Notifications.user_id==self.user.result.user_id, Notifications.notification_read==read).order_by(desc(Notifications.notification_id)))
        result = notifications if notifications else []
        return NotificationResponse(detail="success", result=result)
    

    async def notification_check(self, notification_id:int) -> None:
        if not await self.db.fetch_one(query=select(Notifications).where(Notifications.notification_id==notification_id, Notifications.user_id==self.user.result.user_id)):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your notification")


    async def notification_read(self, notification_id:int) -> NotificationResponse:
        await self.notification_check(notification_id=notification_id)
        result = [await self.db.fetch_one(query=update(Notifications).where(Notifications.notification_id==notification_id).values(notification_read=True).returning(Notifications))]
        return NotificationResponse(detail="success", result=result)
    

    async def notification_delete(self, notification_id:int):
        await self.notification_check(notification_id=notification_id)
        await self.db.execute(query=delete(Notifications).where(Notifications.notification_id==notification_id))
        return Response(detail="success")
    

    async def notification_make_all(self) -> None:
        quizzes = await self.db.fetch_all(query=select(Quizzes))
        if quizzes:
            for quiz in quizzes:
                members = await self.db.fetch_all(query=select(Members).where(Members.company_id == quiz.company_id))
                for member in members:
                    query = select(Statistics).where(Statistics.user_id == member.user_id, Statistics.quiz_id == quiz.quiz_id).order_by(desc(Statistics.statistic_id)).limit(1)
                    statistic = await self.db.fetch_one(query=query)
                    if statistic:
                        next_time = statistic.quiz_passed_at + timedelta(days=quiz.quiz_frequency)
                        if next_time <= date.today():
                            continue
                    company = await self.db.fetch_one(query=select(Companies).where(Companies.company_id == quiz.company_id))
                    await self.db.execute(query=insert(Notifications).values(user_id = member.user_id, 
                                                                             company_id = member.company_id, 
                                                                             quiz_id = quiz.quiz_id, 
                                                                             notification_time = datetime.utcnow(), 
                                                                             notification_content = f"You can take a quiz '{quiz.quiz_name}' from company '{company.company_name}'",
                                                                             notification_read = False))
                    