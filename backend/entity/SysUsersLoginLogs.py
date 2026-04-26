from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SysUsersLoginLogs(Base):
    __tablename__ = "sys_users_login_logs"
    id = Column('id', Integer, primary_key=True, nullable=False, comment="主键id")
    refresh_id = Column('refresh_id', String, primary_key=False, nullable=False, comment="刷新token的id")
    name = Column('name', String, primary_key=False, nullable=False, comment="登录设备名称")
    refresh_token = Column('refresh_token', String, primary_key=False, nullable=False, comment="刷新token")
    ip = Column('ip', String, primary_key=False, nullable=False, comment="登录IP")
    create_date = Column('create_date', Date, primary_key=False, nullable=False, comment="登录日期")
    update_date = Column('update_date', Date, primary_key=False, nullable=False, comment="活跃时间")
    user_id = Column('user_id', Date, primary_key=False, nullable=False, comment="用户id")
