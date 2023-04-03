from core.connections               import get_db
from core.security                  import get_current_user
from databases                      import Database
from fastapi                        import APIRouter, Depends
from schemas.user_schema            import UserResponse
from schemas.notification_schema    import *
from services.notification_service  import NotificationService


router = APIRouter()


@router.get('/my/', response_model=NotificationResponse)
async def get_all_notifications(user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> NotificationResponse:
    return await NotificationService(db=db, user=user).notification_get()


@router.get('/my/read/', response_model=NotificationResponse)
async def get_read_notifications(user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> NotificationResponse:
    return await NotificationService(db=db, user=user).notification_get(read=True)
 

@router.get('/my/unread/', response_model=NotificationResponse)
async def get_unread_notifications(user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> NotificationResponse:
    return await NotificationService(db=db, user=user).notification_get(read=False)
 

@router.put('/{notification_id}/read/', response_model=NotificationResponse)
async def read_notification(notification_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> NotificationResponse:
    return await NotificationService(db=db, user=user).notification_read(notification_id=notification_id)


@router.delete('/{notification_id}/delete/', response_model=Response)
async def read_notification(notification_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> Response:
    return await NotificationService(db=db, user=user).notification_delete(notification_id=notification_id)
