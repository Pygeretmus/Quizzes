from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def health():
    return {
             "status_code": 200,
             "detail": "ok",
             "result": "working"
           }