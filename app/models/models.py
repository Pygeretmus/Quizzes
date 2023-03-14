from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Users(Base):
    __tablename__ = 'Users'
    user_id = Column("user_id", Integer, primary_key=True)
    user_name = Column("user_name", String, nullable=False)
    user_password = Column("user_password", String, nullable=False)
    user_email = Column("user_email", String, unique=True, nullable=False)
    user_status = Column("user_status", String, nullable=True)
    user_registred_at = Column("user_registred_at", DateTime, nullable=False)