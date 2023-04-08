from sqlalchemy                 import Column, Integer, String, DateTime, ForeignKey, ARRAY, Float, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Users(Base):
    __tablename__       = 'Users'
    user_id             = Column("user_id", Integer, primary_key=True)
    user_name           = Column("user_name", String, nullable=False)
    user_password       = Column("user_password", String, nullable=False)
    user_email          = Column("user_email", String, unique=True, nullable=False)
    user_registred_at   = Column("user_registred_at", DateTime, nullable=False)


class Companies(Base):
    __tablename__       = 'Companies'
    company_id          = Column("company_id", Integer, primary_key=True)
    company_name        = Column("company_name", String, nullable=False)
    company_description = Column("company_description", String, nullable=True)
    company_owner_id    = Column("company_owner_id", ForeignKey('Users.user_id'), nullable=False)


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
    role                = Column("role", String, nullable=False)


class Quizzes(Base):
    __tablename__       = 'Quizzes'
    quiz_id             = Column("quiz_id", Integer, primary_key=True)
    quiz_name           = Column("quiz_name", String, nullable=False)
    quiz_frequency      = Column("quiz_frequency", Integer, nullable=False)
    company_id          = Column("company_id", ForeignKey('Companies.company_id', ondelete='CASCADE'), nullable=False)


class Questions(Base):
    __tablename__       = 'Questions'
    question_id         = Column("question_id", Integer, primary_key=True)
    question_name       = Column("question_name", String, nullable=False)
    question_answers    = Column("question_answers", ARRAY(String), nullable=False)
    question_right      = Column("question_right", String, nullable=False)
    quiz_id             = Column("quiz_id", ForeignKey('Quizzes.quiz_id', ondelete='CASCADE'), nullable=False)


class Statistics(Base):
    __tablename__           = 'Statistics'
    statistic_id            = Column("statistic_id", Integer, primary_key=True)
    company_id              = Column("company_id", Integer, nullable=False)
    user_id                 = Column("user_id", ForeignKey('Users.user_id', ondelete='CASCADE'), nullable=False)
    quiz_id                 = Column("quiz_id", Integer, nullable=False)
    quiz_questions          = Column("quiz_questions", Integer, nullable=False)
    quiz_right_answers      = Column("quiz_right_answers", Integer, nullable=False)
    quiz_average            = Column("quiz_average", Float, nullable=False)
    quizzes_questions       = Column("quizzes_questions", Integer, nullable=False)
    quizzes_right_answers   = Column("quizzes_right_answers", Integer, nullable=False)
    quizzes_average         = Column("quizzes_average", Float, nullable=False)
    company_questions       = Column("company_questions", Integer, nullable=False)
    company_right_answers   = Column("company_right_answers", Integer, nullable=False)
    company_average         = Column("company_average", Float, nullable=False)
    all_questions           = Column("all_questions", Integer, nullable=False)
    all_right_answers       = Column("all_right_answers", Integer, nullable=False)
    all_average             = Column("all_average", Float, nullable=False)
    quiz_passed_at          = Column("quiz_passed_at", Date, nullable=False)


class Notifications(Base):
    __tablename__           = 'Notifications'
    notification_id         = Column("notification_id", Integer, primary_key=True)
    user_id                 = Column("user_id", ForeignKey('Users.user_id', ondelete='CASCADE'), nullable=False)
    company_id              = Column("company_id", ForeignKey('Companies.company_id', ondelete='CASCADE'), nullable=False)
    quiz_id                 = Column("quiz_id", ForeignKey('Quizzes.quiz_id', ondelete='CASCADE'), nullable=False)
    notification_time       = Column("notification_time", DateTime, nullable=False)
    notification_read       = Column("notification_read", Boolean, nullable=False)
    notification_content    = Column("notification_content", String, nullable=False)