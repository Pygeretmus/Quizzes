from databases                          import Database
from fastapi                            import HTTPException, status
from models.models                      import Notifications
from schemas.user_schema                import UserResponse
from schemas.notification_schema        import *
from sqlalchemy                         import select, delete, update, desc


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