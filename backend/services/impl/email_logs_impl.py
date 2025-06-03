import datetime
import json
import time

from dbinfo import DatabaseSession
from dto import EmailUserDTO
from entity import EmailLogs
from utils import DbTools
from utils import ReturnTool
from utils import SendMail


def api_send_email_find_list_page_service(page_size, page_index, search_criteria):
    with DatabaseSession() as session:
        query = session.query(EmailLogs)
        # 使用公用方法动态添加搜索条件
        query = DbTools.apply_filters(query, EmailLogs, search_criteria)
        # 根据需要应用过滤器
        paginated_data = DbTools.find_list_page(query, page_size, page_index)
        return ReturnTool.SuccessReturn(paginated_data)


def api_find_users(key):
    with DatabaseSession() as session:
        query = session.query(EmailUserDTO)
        # 使用公用方法动态添加搜索条件
        search_query = json.dumps({"user_state": {"value": 1, "operator": "eq"}})
        if key is not None:
            search_query = json.dumps({"logic_operator": "and", "nick_name": {"value": key, "operator": "like"},
                                       "user_state": {"value": "1", "operator": "eq"}})
        query = DbTools.apply_filters(query, EmailUserDTO, search_query)
        # 根据需要应用过滤器
        paginated_data = DbTools.queryAll(query)
        return ReturnTool.SuccessReturn(paginated_data)


def api_delete_ids_service(ids):
    id_list = ids.split(',')
    with DatabaseSession() as session:
        session.query(EmailLogs).filter(EmailLogs.id.in_(id_list)).delete()
        session.commit()
        return ReturnTool.SuccessReturn()


def api_send_email_service(request_data):
    with DatabaseSession() as session:
        now = datetime.datetime.fromtimestamp(time.time())
        request_data['create_date'] = now
        users_email = request_data['send_users']
        for email in users_email:
            SendMail.send_email(email, request_data['subject'], request_data['body'], True)
        request_data['send_users'] = json.dumps(users_email)
        DbTools.saveOrUpdate(session, request_data, EmailLogs)
        return ReturnTool.SuccessReturn()
