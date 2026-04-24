from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from utils import Config

# 1. 构建URL对象（替代手动拼接字符串）
db_url = URL.create(
    drivername="mysql+pymysql",  # 数据库驱动
    username=Config.mysqlUser,
    password=Config.mysqlPWD,  # 无需手动URL编码！URL.create会自动处理特殊字符
    host=Config.mysqlAddress,
    port=Config.mysqlPort,
    database=Config.mysqlDataBase,
    query={"charset": "utf8mb4"}  # URI参数（编码）
)
# 2. 创建引擎（参数与增强版一致）
engine = create_engine(
    db_url,  # 用URL对象替代字符串URI
    pool_recycle=300,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    connect_args={
        "use_unicode": True,
        "connect_timeout": 10
    }
    # , echo=True # 使用心跳回收机制, 打开sql日志记录
)
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
