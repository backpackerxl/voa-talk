from services.impl import model_config_impl

from utils import ReturnTool

from utils import Config


def api_query_page_service(request):
    page_size = request.args.get('pageSize', default=Config.PageSize, type=int)
    page_index = request.args.get('pageIndex', default=Config.PageIndex, type=int)
    search_criteria = request.args.get('search_criteria')
    return model_config_impl.api_query_list_page_impl(page_size, page_index, search_criteria)

def api_list_page(request):
    search_criteria = request.args.get('search_criteria')
    return model_config_impl.api_list_impl(search_criteria)

def api_delete_ids_service(request):
    request_data = request.get_json()
    if request_data.get("id") is None:
        return ReturnTool.ErrorReturn("id为空")
    ids = request_data.get("id")
    return model_config_impl.api_delete_ids_impl(ids)


def api_save_or_update_service(request):
    request_data = request.get_json()
    return model_config_impl.api_save_or_update_impl(request_data)


