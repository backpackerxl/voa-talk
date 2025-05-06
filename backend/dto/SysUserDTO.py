from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SysUserDTO(Base):
    __tablename__ = "sys_user"
    avatar = Column('avatar', String, primary_key=False, nullable=True, comment="头像")
    create_date = Column('create_date', Date, primary_key=False, nullable=True, comment="创建日期")
    create_user = Column('create_user', String, primary_key=False, nullable=True, comment="创建人")
    id = Column('id', Integer, primary_key=True, nullable=False, comment="主键id")
    last_login_time = Column('last_login_time', String, primary_key=False, nullable=True, comment="最后登录时间")
    nick_name = Column('nick_name', String, primary_key=False, nullable=False, comment="姓名")
    remark = Column('remark', String, primary_key=False, nullable=True, comment="备注")
    super_admin = Column('super_admin', Integer, primary_key=False, nullable=True, comment="是否超级管理员(0否，1是)")
    update_date = Column('update_date', Date, primary_key=False, nullable=True, comment="修改日期")
    update_user = Column('update_user', String, primary_key=False, nullable=True, comment="修改用户")
    user_name = Column('user_name', String, primary_key=False, nullable=False, comment="用户名")
    email = Column('email', String, primary_key=False, nullable=True, comment="邮箱")
    user_state = Column('user_state', Integer, primary_key=False, nullable=True, comment="账户状态(0：停用，1：正常)")
