from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class EmailLogs(Base):
    __tablename__ = "email_logs"
    id = Column('id', Integer, primary_key=True, nullable=False, comment="主键id")
    subject = Column('subject', String, primary_key=False, nullable=False, comment="邮件名称")
    body = Column('body', String, primary_key=False, nullable=False, comment="邮件内容")
    send_users = Column('send_users', Integer, primary_key=False, nullable=False, comment="发送人json字符串")
    create_date = Column('create_date', Date, primary_key=False, nullable=False, comment="创建日期")
