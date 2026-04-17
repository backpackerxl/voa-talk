from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SysUserWebAuth(Base):
    __tablename__ = "sys_users_webauth"
    id = Column('id', Integer, primary_key=True, nullable=False, comment="主键id")
    user_id = Column('user_id', Integer, primary_key=False, nullable=False, comment="用户id")
    content = Column('content', String, primary_key=False, nullable=False, comment="服务端验证数据")
    type = Column('type', String, primary_key=False, nullable=False,
                  comment="服务端验证数据类型（0：生物识别，1：opt码，2：一次性恢复码）")
    name = Column('name', String, primary_key=False, nullable=False, comment="生物识别名称")
    create_date = Column('create_date', Date, primary_key=False, nullable=False, comment="创建日期")
    update_date = Column('update_date', Date, primary_key=False, nullable=False, comment="更新日期")
