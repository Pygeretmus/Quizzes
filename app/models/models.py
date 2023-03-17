from sqlalchemy                 import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Users(Base):
    __tablename__       = 'Users'
    user_id             = Column("user_id", Integer, primary_key=True)
    user_name           = Column("user_name", String, nullable=False)
    user_password       = Column("user_password", String, nullable=False)
    user_email          = Column("user_email", String, unique=True, nullable=False)
    user_status         = Column("user_status", String, nullable=True)
    user_registred_at   = Column("user_registred_at", DateTime, nullable=False)


class Companies(Base):
    __tablename__       = 'Companies'
    company_id          = Column("company_id", Integer, primary_key=True)
    company_name        = Column("company_name", String, nullable=False)
    company_description = Column("company_description", String, nullable=True)
    company_owner_id    = Column("company_owner_id", ForeignKey('Users.user_id', ondelete = "CASCADE"), nullable=False)


class Invites(Base):
    __tablename__       = 'Invites'
    invite_id           = Column("invite_id", Integer, primary_key=True)
    to_user_id          = Column("to_user_id", Integer, ForeignKey('Users.user_id', ondelete = "CASCADE"), nullable=False)
    from_company_id     = Column("from_company_id", Integer, ForeignKey('Companies.company_id', ondelete = "CASCADE"), nullable=False)
    invite_message      = Column("invite_message", String, nullable=False)


class Requests(Base):
    __tablename__       = 'Requests'
    request_id          = Column("request_id", Integer, primary_key=True)
    to_company_id       = Column("to_company_id", Integer, ForeignKey('Companies.company_id', ondelete = "CASCADE"), nullable=False)
    from_user_id        = Column("from_user_id", Integer, ForeignKey('Users.user_id', ondelete = "CASCADE"), nullable=False)
    request_message     = Column("request_message", String, nullable=False)


class Members(Base):
    __tablename__       = 'Members'
    useless_id          = Column("useless_id", Integer, primary_key=True)
    user_id             = Column("user_id", ForeignKey('Users.user_id', ondelete='CASCADE'), nullable=False)
    company_id          = Column("company_id", ForeignKey('Companies.company_id', ondelete='CASCADE'), nullable=False)