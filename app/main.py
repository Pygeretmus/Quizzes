from fastapi import FastAPI
import uvicorn
from decouple import config
import connections


app = FastAPI()


@app.on_event("startup")
async def databases_connect():
    await connections.redis_connect()
    await connections.db_connect()

@app.on_event("shutdown")
async def databases_close():
    await connections.redis.close()
    await connections.db_disconnect()

@app.get('/')
async def health():
    return {
             "status_code": 200,
             "detail": "ok",
             "result": "working"
           }


if __name__ == '__main__':
    uvicorn.run('main:app', host=config('app_host', cast=str), port=config('app_port', cast=int), reload=True)
