from pydantic import BaseModel
from datetime import datetime


class Notification(BaseModel):
    user_id: int
    company_id: int    
    quiz_id: int
    notification_id: int
    notification_time: datetime
    notification_read: bool
    notification_content: str

    class Config:
        orm_mode = True


class Response(BaseModel):
    detail: str


class NotificationResponse(Response):
    result: list[Notification]