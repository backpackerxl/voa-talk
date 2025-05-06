import json
import traceback
from datetime import datetime

from sqlalchemy import or_, desc, asc, and_

from utils.BusinessException import BusinessException


def format_model_data(model_instance):
    """
    将数据库模型实例格式化为字典，包括其所有的属性。
    :param model_instance: 数据库模型实例
    :return: 格式化后的字典
    """
    data = {}
    for column in model_instance.__table__.columns:
        data[column.name] = getattr(model_instance, column.name)
    return data


def convert_timestamps_in_dict(record):
    """
    将字典中的时间戳或 datetime 对象转换为日期字符串。
    13位时间戳转换为日期字符串，datetime 对象转换为 'YYYY-MM-DD HH:MM:SS' 格式。
    :param record: 字典
    :return: 转换后的字典
    """
    for key, value in record.items():
        if isinstance(value, int) and len(str(value)) == 13:
            # record[key] = datetime.fromtimestamp(value / 1000).strftime('%Y-%m-%d %H:%M:%S')
            record[key] = datetime.fromtimestamp(value / 1000).strftime('%Y-%m-%d')
        elif isinstance(value, datetime):
            # 将 datetime 对象转换为 'YYYY-MM-DD HH:MM:SS' 日期格式字符串
            record[key] = value.strftime('%Y-%m-%d %H:%M:%S')
    return record


def find_list_page(query, page_size, page_index):
    """
    分页查询
    :param query: 查询对象
    :param page_size: 页大小
    :param page_index: 页码
    :return: 分页结果
    """
    total_count = query.count()
    currentPage = query.limit(page_size).offset((page_index - 1) * page_size).all()
    records = [convert_timestamps_in_dict(format_model_data(product)) for product in currentPage]
    total_pages = (total_count + page_size - 1) // page_size
    return {"total_count": total_count, "records": records, "total_pages": total_pages}


def queryAll(query):
    """
    查询全部
    :param query: 查询对象
    :return: 查询结果
    """
    current = query.all()
    records = [convert_timestamps_in_dict(format_model_data(product)) for product in current]
    return records


# 新增或者编辑数据
def saveOrUpdate(session, requestBody, model, commit=True):
    """
    新增或者编辑数据，只更新model中存在的属性。
    :param session: SQLAlchemy数据库会话
    :param requestBody: 请求体，包含需要更新或新增的数据
    :param model: 数据库模型
    :param commit: 是否自动提交，默认为True
    :return: 保存结果，为model的一个实例
    """
    if requestBody.get("id"):
        print("编辑")

        # 尝试通过ID获取现有记录
        model_instance = session.query(model).get(requestBody.get("id"))
        if model_instance:
            # 更新现有记录的属性
            for key in requestBody:
                if hasattr(model_instance, key):
                    # 只有当model实例具有该属性时才更新
                    setattr(model_instance, key, requestBody[key])
            if commit:
                print("自动提交")
                try:
                    session.commit()
                except:
                    print(traceback.format_exc())
                    session.rollback()
                    raise BusinessException(-18690, "数据更新失败")
        else:
            # 如果通过ID找不到实例，则返回False
            raise BusinessException(404, "数据没有找到")
    else:
        print("新增")
        # 为新增记录准备一个字典，仅包含模型定义的属性
        valid_fields = {key: value for key, value in requestBody.items() if hasattr(model, key)}
        model_instance = model(**valid_fields)
        session.add(model_instance)
        if commit:
            print("自动提交")
            try:
                session.commit()
            except:
                print(traceback.format_exc())
                session.rollback()
                raise BusinessException(-18690, "数据更新失败")
    return model_instance


# 批量新增数据
def bulk_insert(session, request_body_list, model, commit=True):
    """
    批量新增数据。
    :param session: SQLAlchemy数据库会话
    :param request_body_list: 请求体列表，每个元素包含需要新增的数据
    :param model: 数据库模型
    :return: 批量保存的结果，为model的实例列表
    """
    model_instances = []

    for requestBody in request_body_list:
        # 为每条记录准备一个字典，仅包含模型定义的属性
        valid_fields = {key: value for key, value in requestBody.items() if hasattr(model, key)}
        model_instance = model(**valid_fields)
        model_instances.append(model_instance)

    # 使用add_all批量添加所有实例
    session.add_all(model_instances)
    try:
        if commit:
            session.commit()
    except:
        print(traceback.format_exc())
        session.rollback()
        raise BusinessException(-18690, "数据更新失败")
    return model_instances


def apply_filters(query, model, filters):
    """
    动态添加搜索条件
    :param query: SQLAlchemy Query对象
    :param model: SQLAlchemy 模型类
    :param filters: 字典形式的搜索条件，key为模型的字段名，value为包含搜索值和查询类型的字典
    {'name': {'value': 'John', 'is_fuzzy': True}} name是字段名，value是搜索值，is_fuzzy是是否模糊查询
    :return: 处理后的查询对象
    """
    if not filters:
        return query

    try:
        filters = json.loads(filters)
    except (json.JSONDecodeError, TypeError):
        return query

    if not isinstance(filters, dict) or len(filters) == 0:
        return query

    filter_conditions = []
    logic_operator = filters.pop('logic_operator', 'and')  # 默认为 'and'

    for key, condition in filters.items():
        if not hasattr(model, key):
            continue  # 跳过无效字段

        value = condition.get('value')
        operator = condition.get('operator', 'eq')  # 默认为等于 ('eq')

        if value is None or value == '':
            continue

        field = getattr(model, key)
        try:
            if operator == 'eq':
                filter_conditions.append(field == value)
            elif operator == 'ne':
                filter_conditions.append(field != value)
            elif operator == 'gt':
                filter_conditions.append(field > value)
            elif operator == 'lt':
                filter_conditions.append(field < value)
            elif operator == 'like':
                filter_conditions.append(field.like(f'%{value}%'))
            elif operator == 'in':
                filter_conditions.append(field.in_(value))
            elif operator == 'not_in':
                filter_conditions.append(~field.in_(value))
            else:
                raise ValueError(f"Unsupported operator: {operator}")
        except Exception as e:
            print(f"Error processing filter for field '{key}': {e}")
            continue

    if filter_conditions:
        if logic_operator == 'and':
            query = query.filter(and_(*filter_conditions))
        elif logic_operator == 'or':
            query = query.filter(or_(*filter_conditions))
        else:
            raise ValueError(f"Unsupported logic operator: {logic_operator}")
    # 处理排序
    sort = filters.pop('sort', None)
    if sort:
        sort_field = sort.get('field')
        sort_order = sort.get('order', 'asc')
        if sort_field and hasattr(model, sort_field):
            field = getattr(model, sort_field)
            if sort_order.lower() == 'asc':
                query = query.order_by(field.asc())
            elif sort_order.lower() == 'desc':
                query = query.order_by(field.desc())
            else:
                print(f"Unsupported sort order: {sort_order}")

    return query


def get_sorted_query(session, model, sort_by, order):
    """
    根据排序字段和顺序返回排序后的查询对象
    :param session: SQLAlchemy Session对象
    :param model: SQLAlchemy 模型类
    :param sort_by: 排序字段
    :param order: 排序顺序（'asc' 或 'desc'）
    :return: 排序后的查询对象
    """
    if order == 'desc':
        query = session.query(model).order_by(desc(getattr(model, sort_by)))
    elif order == 'asc':
        query = session.query(model).order_by(asc(getattr(model, sort_by)))
    else:
        query = session.query(model)
    return query
