import uvicorn

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.connections               import get_db, redis_close, redis_connect, get_redis
from databases                      import Database
from decouple                       import config
from fastapi                        import FastAPI, Depends
from routers                        import quiz_route, user_route, auth, company_route, invite_route, request_route, data_route, analytics_route, notifications_route
from schemas.user_schema            import *
from services.notification_service  import NotificationService


app = FastAPI()
app.include_router(analytics_route.router, prefix='/analytics', tags=["Analytics"])
app.include_router(auth.router, prefix='/auth', tags=["Auth"])
app.include_router(company_route.router, prefix='', tags=["Company"])
app.include_router(data_route.router, prefix='/data', tags=["Data"])
app.include_router(invite_route.router, prefix='/invite', tags=["Invite"])
app.include_router(notifications_route.router, prefix='/notifications', tags=["Notifications"])
app.include_router(quiz_route.router, prefix='', tags= ["Quiz"])
app.include_router(request_route.router, prefix='/request', tags=["Request"])
app.include_router(user_route.router, prefix='', tags= ["User"])


scheduler = AsyncIOScheduler()


async def make_notifications():
    db = get_db()
    await NotificationService(db=db).notification_make_all()


@app.on_event("startup")
async def databases_connect():
    await redis_connect()  
    databases = get_db()
    await databases.connect()
    scheduler.add_job(make_notifications, 'cron', hour=2, minute=0)
    scheduler.start()


@app.on_event("shutdown")
async def databases_close():
    scheduler.shutdown()
    await redis_close()  
    databases = get_db()
    await databases.disconnect()
    



@app.get('/')
async def health():
    return {
             "status_code": 200,
             "detail": "ok",
             "result": "working"
           }





if __name__ == '__main__':
    uvicorn.run('main:app', host=config('app_host', cast=str), port=config('app_port', cast=int), reload=True)