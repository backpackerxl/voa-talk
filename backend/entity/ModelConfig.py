from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ModelConfig(Base):
    __tablename__ = "model_config"
    id = Column('id', Integer, primary_key=True, nullable=False, comment="主键id")
    name = Column('name', String, primary_key=False, nullable=False, comment="模型名称")
    desc = Column('desc', String, primary_key=False, nullable=True, comment="模型描述")
    req_url = Column('req_url', String, primary_key=False, nullable=False, comment="接口请求地址")
    api_key = Column('api_key', String, primary_key=False, nullable=False, comment="API接口Key")
    model_id = Column('model_id', String, primary_key=False, nullable=False, comment="模型ID")
    create_date = Column('create_date', Date, primary_key=False, nullable=True, comment="创建日期")
    update_date = Column('update_date', Date, primary_key=False, nullable=True, comment="修改日期")
    sort = Column('sort', Integer, primary_key=False, nullable=True, comment="排序")
