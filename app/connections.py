import aioredis
from decouple import config
from databases import Database
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine


DATABASE_URL = f"postgresql+asyncpg://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}@{config('POSTGRES_HOST')}:{config('POSTGRES_PORT')}/{config('POSTGRES_DATABASE')}" 
db = Database(DATABASE_URL)
redis = False
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
metadata = sqlalchemy.MetaData()

def get_db():
    return db

async def redis_connect():
    global redis
    redis = aioredis.from_url("redis://redis")
