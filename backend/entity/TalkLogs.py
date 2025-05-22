from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TalkLogs(Base):
    __tablename__ = "talk_logs"
    id = Column('id', Integer, primary_key=True, nullable=False, comment="主键id")
    talk_id = Column('talk_id', Integer, primary_key=False, nullable=False, comment="对话ID")
    resp_content = Column('resp_content', String, primary_key=False, nullable=False, comment="模型响应信息")
    req_content = Column('req_content', String, primary_key=False, nullable=False, comment="用户输入的信息")
    img = Column('img', String, primary_key=False, nullable=True, comment="用户上传的图片")
    create_date = Column('create_date', Date, primary_key=False, nullable=True, comment="创建日期")
    tokens = Column('tokens', Date, primary_key=False, nullable=False, comment="大模型token消耗")
