from fastapi import FastAPI
import uvicorn
from decouple import config
from core.connections import get_db, redis_close, redis_connect
from routers.user_route import router 
from schemas.user_schema import *


app = FastAPI()
app.include_router(router, prefix='')


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
