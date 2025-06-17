import os
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

password = os.getenv('MYSQL_PASSWORD')
DATABASE_URI = f'mysql+pymysql://root:{password}@127.0.0.1:3308/ai_chat'
# engine = create_engine(DATABASE_URI, pool_recycle=300, echo=True)  # 使用心跳回收机制, 打开sql日志记录
engine = create_engine(DATABASE_URI, pool_recycle=300)  # 使用心跳回收机制
Session = sessionmaker(bind=engine)


def DatabaseSession():
    return Session()


# SQL语句执行函数
def execute_sql(sql):
    session = DatabaseSession()
    result = session.execute(text(sql)).all()
    session.close()
    return result
# https://pypi.tuna.tsinghua.edu.cn/simple/
