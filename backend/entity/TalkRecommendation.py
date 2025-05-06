from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TalkRecommendation(Base):
    __tablename__ = "talk_recommendation"
    id = Column('id', Integer, primary_key=True, nullable=False, comment="主键id")
    talk_id = Column('talk_id', Integer, primary_key=False, nullable=False, comment="对话ID")
    content = Column('content', String, primary_key=False, nullable=False, comment="推荐内容")
