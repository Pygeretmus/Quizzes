import aioredis

from databases  import Database
from decouple   import config



DATABASE_URL = f"postgresql+asyncpg://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}@{config('POSTGRES_HOST')}:{config('POSTGRES_PORT')}/{config('POSTGRES_DB')}" 
db = Database(DATABASE_URL)
redis = False


def get_db() -> Database:
    return db


def get_redis() -> Database:
    return redis


async def redis_connect():
    global redis
    redis = await aioredis.from_url("redis://redis/0")


async def redis_close():
    await redis.close()