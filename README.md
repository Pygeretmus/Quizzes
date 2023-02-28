# internship
## Main.py
Запуск сервера - python main.py

## test_main.py
Запуск тестов - python -m pytest

## Docker
Построение изображения - docker build -t myimage .
Построение контейнера - docker run -d --name mycontainer -p 80:80 myimage

## Docker-compose
Запуск контейнера вместе с построением - docker-compose up --build

## Alembic
Создание миграции - docker-compose exec web alembic revision --autogenerate -m "комментарий"

Обновление до последней миграции - docker-compose exec web alembic upgrade head