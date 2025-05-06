import datetime
import time

from dbinfo import DatabaseSession
from entity import ModelConfig
from utils import DbTools
from utils import ReturnTool


def api_query_list_page_impl(page_size, page_index, search_criteria):
    with DatabaseSession() as session:
        query = session.query(ModelConfig)
        # 使用公用方法动态添加搜索条件
        query = DbTools.apply_filters(query, ModelConfig, search_criteria)
        # 根据需要应用过滤器
        paginated_data = DbTools.find_list_page(query, page_size, page_index)
        return ReturnTool.SuccessReturn(paginated_data)


def api_delete_ids_impl(ids):
    """
    删除配置
    """
    id_list = ids.split(',')
    with DatabaseSession() as session:
        session.query(ModelConfig).filter(ModelConfig.id.in_(id_list)).delete()
        session.commit()
        return ReturnTool.SuccessReturn()


def api_save_or_update_impl(request_data):
    """
    配置新增或编辑
    """
    with DatabaseSession() as session:
        # 使用 saveOrUpdate 函数
        now = datetime.datetime.fromtimestamp(time.time())
        if request_data.get('id') is None:
            request_data['create_date'] = now
            request_data['update_date'] = now
        else:
            request_data['update_date'] = now

        result = DbTools.saveOrUpdate(session, request_data, ModelConfig)
        if result:
            return ReturnTool.SuccessReturn()
        else:
            return ReturnTool.ErrorReturn('数据没有找到')


def api_list_impl(search_criteria):
    with DatabaseSession() as session:
        query = session.query(ModelConfig)
        # 使用公用方法动态添加搜索条件
        query = DbTools.apply_filters(query, ModelConfig, search_criteria)
        # 根据需要应用过滤器
        data = DbTools.queryAll(query)
        data = [{"id": mc['id'], "name": mc['name']} for mc in data]
        return ReturnTool.SuccessReturn(data)
