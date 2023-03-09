import asyncio
import pytest_asyncio

from typing import AsyncGenerator
from starlette.testclient import TestClient
from databases import Database
from sqlalchemy.ext.asyncio import create_async_engine
from httpx import AsyncClient

#import your app
from app.main import app, get_db
#import your metadata
from app.models.models import Base
#import your test urls for db
from decouple import config

DATABASE_URL = f"postgresql+asyncpg://{config('TEST_USER')}:{config('TEST_PASSWORD')}@{config('TEST_HOST')}:{config('POSTGRES_PORT')}/{config('TEST_DB')}" 
test_db = Database(DATABASE_URL)


def override_get_db() -> Database:
    return test_db


app.dependency_overrides[get_db] = override_get_db


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
    await test_db.connect()
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await test_db.disconnect()
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
