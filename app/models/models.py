from connections import get_db, metadata
from sqlalchemy import Column, Integer, String, Table

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("password", String),
    Column("email", String, unique=True),
)