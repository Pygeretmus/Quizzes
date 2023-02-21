# internship
## Main.py
Содержит в себе:
from fastapi import FastAPI - импорт класса FastAPI, который предоставляет дальнейшую функциональность
app = FastAPI() - создание "представителя" класса FasrAPI для дальнейшего использования методов класса
@app.get('/') - декоратор вызова функции при GET запросе по заданной ссылке
дальше с помощью uvicorn main:app запускается приложение, чтобы не запускать его каждый раз можно добавить тэг --reload, так сервер будет перезапускаться после каждого изменения документа.
if __name__ == '__main__':
    uvicorn.run('main:app', host=config('host_port', cast=str), port=config('app_port', cast=int), reload=True)
При комманде 'python main.py' после полного просмотра файла запускает сервер с заданными портом и хостом. 

## test_main.py
Содержит в себе:
from httpx import AsyncClient - импорт асинхронного HTTP-клиента, с помощью чего можно выполнять HTTP-запросы.
response = await ac.get("/") - HTTP-запрос с ожиданием ответа от сервера
assert response.status_code == 200 - Обработка результатов
assert response.json() == data -                            запроса
python -m pytest - запускает тесты
