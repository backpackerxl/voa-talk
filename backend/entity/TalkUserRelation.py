from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TalkUserRelation(Base):
    __tablename__ = "talk_user_relation"
    id = Column('id', Integer, primary_key=True, nullable=False, comment="主键id")
    user_id = Column('user_id', Integer, primary_key=False, nullable=False, comment="用户ID")
    talk_id = Column('talk_id', Integer, primary_key=False, nullable=False, comment="对话ID")
    talk_name = Column('talk_name', String, primary_key=False, nullable=False, comment="对话名称")
    nick_name = Column('nick_name', String, primary_key=False, nullable=False, comment="用户昵称")
    create_date = Column('create_date', Date, primary_key=False, nullable=True, comment="创建日期")
