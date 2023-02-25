import aioredis
from decouple import config
import databases

db = databases.Database(f"postgresql://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}@{config('POSTGRES_HOST')}:{config('POSTGRES_PORT')}/{config('POSTGRES_DATABASE')}")
redis = False

def get_db():
    return db

async def redis_connect():
    global redis
    redis = aioredis.from_url("redis://redis")
