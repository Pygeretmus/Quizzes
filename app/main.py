from fastapi import FastAPI
import uvicorn
from decouple import config


app = FastAPI()

@app.get('/')
async def health():
    return {
             "status_code": 200,
             "detail": "ok",
             "result": "working"
           }


if __name__ == '__main__':
    uvicorn.run('main:app', host=config('app_host', cast=str), port=config('app_port', cast=int), reload=True)
