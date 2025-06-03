from sqlalchemy import Column
from sqlalchemy import String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class EmailUserDTO(Base):
    __tablename__ = "sys_user"
    id = Column('id', Integer, primary_key=True, nullable=False, comment="主键id")
    avatar = Column('avatar', String, primary_key=False, nullable=True, comment="头像")
    nick_name = Column('nick_name', String, primary_key=False, nullable=False, comment="姓名")
    email = Column('email', String, primary_key=False, nullable=True, comment="邮箱")
    user_state = Column('user_state', Integer, primary_key=False, nullable=True, comment="账户状态(0：停用，1：正常)")
