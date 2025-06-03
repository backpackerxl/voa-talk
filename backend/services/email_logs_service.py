from services.impl import email_logs_impl

from utils import ReturnTool

from utils import Config
from utils.JwtUtils import JWTHandler


def api_send_email_find_list_page_service(request):
    page_size = request.args.get('pageSize', default=Config.PageSize, type=int)
    page_index = request.args.get('pageIndex', default=Config.PageIndex, type=int)
    search_criteria = request.args.get('search_criteria')
    return email_logs_impl.api_send_email_find_list_page_service(page_size, page_index, search_criteria)

def api_find_users(request):
    key = request.args.get('key')
    return email_logs_impl.api_find_users(key)


def api_delete_ids_service(request):
    request_data = request.get_json()
    if request_data.get("id") is None:
        return ReturnTool.ErrorReturn("id为空")
    ids = request_data.get("id")
    return email_logs_impl.api_delete_ids_service(ids)


def api_send_email_service(request):
    request_data = request.get_json()
    return email_logs_impl.api_send_email_service(request_data)
