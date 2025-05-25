import hashlib
import json
import uuid
from datetime import datetime

from dbinfo import DatabaseSession
from decimal import Decimal
from sqlalchemy import or_, text
from dto import SysUserDTO
from entity import SysUser, ModelConfig, TalkLogs
from utils import DbTools, Config, encryptUtils, Tools
from utils import ReturnTool
import bcrypt

from utils import TimeToolClass

from utils import SendMail
from utils.GetChatId import Snowflake
from utils.RedisUtils import RedisHandler
from utils.encryptUtils import aes_decrypt

snowflake = Snowflake(data_center_id=1, worker_id=2)

sql_pool = {
    'top_talk': text("""
        WITH t1 AS (
                SELECT tl.talk_id, SUM(tl.tokens) AS tokens 
                    FROM talk_logs tl 
                    WHERE tl.create_date >= (NOW() - INTERVAL 7 DAY) 
                    GROUP BY tl.talk_id ORDER BY SUM(tl.tokens) DESC LIMIT 6
                )
        SELECT tur.talk_name, t1.tokens FROM t1 LEFT JOIN talk_user_relation tur ON tur.talk_id = t1.talk_id
    """),
    'model_talks': text("""
            WITH t1 AS (
                SELECT rl.model_id, COUNT(rl.id) AS total 
                FROM request_logs rl 
                WHERE rl.create_date BETWEEN :start_time AND :end_time 
                GROUP BY rl.model_id
            )
            SELECT mc.`name`, t1.total AS `value` FROM t1 LEFT JOIN model_config mc ON mc.id = t1.model_id
    """),
    'bar_talks': text("""
                WITH RECURSIVE dates AS (
                    SELECT :start_time AS date
                        UNION ALL
                    SELECT DATE_ADD(date, INTERVAL 1 DAY)
                    FROM dates
                    WHERE date < :end_time
                )
                SELECT 
                    dates.date,
                    COALESCE(COUNT(t.id), 0) AS talk_count
                FROM 
                    dates
                LEFT JOIN 
                    talk_logs t ON dates.date = DATE(t.create_date)
                GROUP BY 
                dates.date
                ORDER BY 
                dates.date;
    """),
    'line_tokens': text("""
                WITH RECURSIVE dates AS (
                    SELECT :start_time AS date
                        UNION ALL
                    SELECT DATE_ADD(date, INTERVAL 1 DAY)
                    FROM dates
                    WHERE date < :end_time
                )
                SELECT 
                    dates.date,
                    COALESCE(SUM(t.tokens), 0) AS tokens_count
                FROM 
                    dates
                LEFT JOIN 
                    talk_logs t ON dates.date = DATE(t.create_date)
                GROUP BY 
                dates.date
                ORDER BY 
                dates.date;
    """)
}


def header_data():
    # 获取当前年份
    current_year = datetime.now().year
    # 创建今年 1 月 1 日 00:00:00 的日期时间对象
    new_year_date = datetime(current_year, 1, 1, 0, 0, 0)
    with DatabaseSession() as session:
        user_count = session.query(SysUser).count()
        model_count = session.query(ModelConfig).count()
        talk_count = session.query(TalkLogs).filter(TalkLogs.create_date >= new_year_date).count()
        return ReturnTool.SuccessReturn({
            'user_count': user_count,
            'model_count': model_count,
            'talk_count': talk_count,
        })


def top_talk():
    with DatabaseSession() as session:
        result = session.execute(sql_pool['top_talk']).mappings().all()
        processed_data = [
            {k: int(v) if isinstance(v, Decimal) else v for k, v in item.items()}
            for item in result
        ]
        return ReturnTool.SuccessReturn(processed_data)


def bar_talks(stm, etm):
    start_time = datetime.strptime(stm, "%Y-%m-%d")
    end_time = datetime.strptime(etm, "%Y-%m-%d")
    with DatabaseSession() as session:
        result = session.execute(sql_pool['bar_talks'],
                                 {'start_time': start_time, 'end_time': end_time}).mappings().all()
        processed_data = [
            {k: int(v) if isinstance(v, Decimal) else v for k, v in item.items()}
            for item in result
        ]
        return ReturnTool.SuccessReturn(processed_data)


def model_talks(stm, etm):
    start_time = datetime.strptime(stm, "%Y-%m-%d")
    end_time = datetime.strptime(etm, "%Y-%m-%d")
    with DatabaseSession() as session:
        result = session.execute(sql_pool['model_talks'],
                                 {'start_time': start_time, 'end_time': end_time}).mappings().all()
        processed_data = [
            {k: int(v) if isinstance(v, Decimal) else v for k, v in item.items()}
            for item in result
        ]
        return ReturnTool.SuccessReturn(processed_data)


def line_tokens(stm, etm):
    start_time = datetime.strptime(stm, "%Y-%m-%d")
    end_time = datetime.strptime(etm, "%Y-%m-%d")
    with DatabaseSession() as session:
        result = session.execute(sql_pool['line_tokens'],
                                 {'start_time': start_time, 'end_time': end_time}).mappings().all()
        processed_data = [
            {k: int(v) if isinstance(v, Decimal) else v for k, v in item.items()}
            for item in result
        ]
        return ReturnTool.SuccessReturn(processed_data)
