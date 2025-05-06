from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RequestLogs(Base):
    __tablename__ = "request_logs"
    id = Column('id', Integer, primary_key=True, nullable=False, comment="主键id")
    user_id = Column('user_id', String, primary_key=False, nullable=False, comment="用户ID")
    model_id = Column('model_id', String, primary_key=False, nullable=False, comment="模型ID")
    create_date = Column('create_date', Date, primary_key=False, nullable=True, comment="创建日期")
