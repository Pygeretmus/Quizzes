import aioredis
from decouple import config
import databases

db = databases.Database(f"postgresql://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}@{config('POSTGRES_HOST')}:{config('POSTGRES_PORT')}/{config('POSTGRES_DATABASE')}")
redis = False

async def db_connect():
    await db.connect()

async def db_disconnect():
    await db.disconnect()

async def redis_connect():
    global redis
    redis = aioredis.from_url("redis://redis")
