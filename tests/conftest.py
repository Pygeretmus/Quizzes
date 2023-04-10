import asyncio
import pytest_asyncio
import aioredis

from typing import AsyncGenerator
from starlette.testclient import TestClient
from databases import Database
from sqlalchemy.ext.asyncio import create_async_engine
from httpx import AsyncClient

#import your app
from app.main import app, get_db, get_redis
from app.services.notification_service import NotificationService

#import your metadata
from app.models.models import Base
#import your test urls for db
from decouple import config


DATABASE_URL = f"postgresql+asyncpg://{config('TEST_USER')}:{config('TEST_PASSWORD')}@{config('TEST_HOST')}:{config('POSTGRES_PORT')}/{config('TEST_DB')}"


test_db = Database(DATABASE_URL)
redis = False

def override_get_db() -> Database:
    return test_db


def override_get_redis():
    return redis

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_redis] = override_get_redis


engine_test = create_async_engine(DATABASE_URL)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
def test_app():
    client = TestClient(app)
    yield client


@pytest_asyncio.fixture(autouse=True, scope='session')
async def prepare_database():
    global redis
    redis = await aioredis.from_url("redis://redis/1")
    await test_db.connect()
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await redis.close()
    await test_db.disconnect()
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope='session')
async def login_user(ac: AsyncClient, users_tokens):
    async def __send_request(user_email: str, user_password: str):
        payload = {
            "user_email": user_email,
            "user_password": user_password,
        }
        response = await ac.post("/auth/login/", json=payload)
        if response.status_code != 200:
            return response
        user_token = response.json().get('result').get('access_token')
        users_tokens[user_email] = user_token
        return response

    return __send_request


@pytest_asyncio.fixture(scope='session')
def users_tokens():
    tokens_store = dict()
    return tokens_store


@pytest_asyncio.fixture(scope='session')
async def notifications():
    db = override_get_db()
    await NotificationService(db=db).notification_make_all()
