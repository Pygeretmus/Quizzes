import uvicorn

from decouple               import config
from core.connections       import get_db, redis_close, redis_connect, get_redis
from fastapi                import FastAPI
from routers                import quiz_route, user_route, auth, company_route, invite_route, request_route
from schemas.user_schema    import *


app = FastAPI()
app.include_router(auth.router, prefix='/auth', tags=["Auth"])
app.include_router(company_route.router, prefix='', tags=["Company"])
app.include_router(invite_route.router, prefix='/invite', tags=["Invite"])
app.include_router(quiz_route.router, prefix='', tags= ["Quiz"])
app.include_router(request_route.router, prefix='/request', tags=["Request"])
app.include_router(user_route.router, prefix='', tags= ["User"])



@app.on_event("startup")
async def databases_connect():
    await redis_connect()  
    databases = get_db()
    await databases.connect()


@app.on_event("shutdown")
async def databases_close():
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
