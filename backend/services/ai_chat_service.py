import json

from services.impl import ai_chat_impl
from utils import Config, ReturnTool
from utils.JwtUtils import JWTHandler
from utils.RedisUtils import RedisHandler


def ai_chat_dialogue_serve(request):
    """
    对话处理类
    :param request:
    :return:
    """
    request_data = request.get_json()
    user_input = request_data.get('user_input')
    model_id = request_data.get('model_id')
    session_id = request_data.get('session_id')
    return ai_chat_impl.ai_chat_dialogue_impl(session_id, user_input, model_id)


def get_req_user(request):
    # 从请求头中获取 token
    token = request.headers.get('token')
    # 创建 JWTHandler 实例
    jwt_handler = JWTHandler()
    # 使用 JWTHandler 的 VerifyToken 方法验证 token
    valid, payload = jwt_handler.VerifyToken(token)
    # 如果 token 无效，抛出 ValueError 异常
    if not valid:
        raise ValueError("无效的令牌")
    return payload


def ai_save_chat_serve(request):
    request_data = request.get_json()
    user_id = get_req_user(request).get("id")
    return ai_chat_impl.ai_save_chat_serve(user_id, request_data)


def save_chat_title(request):
    request_data = request.get_json()
    user_input = request_data.get('user_input')
    model_id = request_data.get('model_id')
    user = get_req_user(request)
    user_id = user.get('id')
    nick_name = user.get('nickName')
    return ai_chat_impl.save_chat_title(user_id, nick_name, user_input, model_id, request_data)


def api_list_page(request):
    # search_criteria = request.args.get('search_criteria')
    # `{"name": {"value": "${state.user_name}", "operator": "like"}, "sort": {"field": "sort", "order": "desc"}}`
    page_size = request.args.get('pageSize', default=Config.PageSize, type=int)
    page_index = request.args.get('pageIndex', default=Config.PageIndex, type=int)
    user_id = get_req_user(request).get('id')
    # print(get_req_uer_id(request))
    search_criteria_dict = {
        "user_id": {"value": user_id, "operator": "eq"},
        "sort": {"field": "create_date", "order": "desc"}
    }
    return ai_chat_impl.api_list_impl(json.dumps(search_criteria_dict), page_size, page_index)


def api_other_user_list_page(request):
    page_size = request.args.get('pageSize', default=Config.PageSize, type=int)
    page_index = request.args.get('pageIndex', default=Config.PageIndex, type=int)
    res = RedisHandler().get_key(request.args.get('bindOtherAccount'))
    if res is None:
        return ReturnTool.ErrorReturn('第三方授权失效！', 400)
    res = JWTHandler().decode_jwt(res)
    data = res['data']
    user_id = data['id'],
    search_criteria_dict = {
        "user_id": {"value": user_id, "operator": "eq"},
        "sort": {"field": "create_date", "order": "desc"}
    }
    resp_data = ai_chat_impl.api_list_impl(json.dumps(search_criteria_dict), page_size, page_index)
    return ReturnTool.SuccessReturn({
        'other_avatar': data['avatar'],
        'other_username': data['userName'],
        'list': resp_data['data']
    })


def api_link_other(request):
    state = request.args.get('state')
    res = RedisHandler().get_key(request.args.get('bindOtherAccount'))
    if res is None:
        return ReturnTool.ErrorReturn('第三方授权失效！', 400)
    res = JWTHandler().decode_jwt(res)
    data = res['data']
    other_user_id = data['id']
    user_id = get_req_user(request).get('id')
    if state == '1':
        return ai_chat_impl.api_link_qq(other_user_id, user_id)
    elif state == '2':
        return ai_chat_impl.api_link_github(other_user_id, user_id)
    else:
        return ReturnTool.ErrorReturn('不支持的第三方绑定！', 500)


def api_no_link_other(request):
    state = request.args.get('state')
    user_id = get_req_user(request).get('id')
    if state == '1':
        return ai_chat_impl.api_no_link_qq_other(user_id)
    elif state == '2':
        return ai_chat_impl.api_no_link_github_other(user_id)
    else:
        return ReturnTool.ErrorReturn('不支持的第三方绑定！', 500)


def one_chat(request):
    talk_id = request.args.get('talk_id')
    search_criteria_dict = {
        "talk_id": {"value": talk_id, "operator": "eq"},
        "sort": {"field": "create_date"}
    }
    return ai_chat_impl.one_chat(json.dumps(search_criteria_dict))


def api_delete_ids_service(request):
    request_data = request.get_json()
    if request_data.get("talk_id") is None:
        return ReturnTool.ErrorReturn("talk_id为空")
    ids = request_data.get("talk_id")
    return ai_chat_impl.api_delete_ids_impl(ids)


def api_update_ids(request):
    request_data = request.get_json()
    talk_id = request_data.get('talk_id')
    return ai_chat_impl.api_update_ids(talk_id, request_data)


def api_query_page_service(request):
    page_size = request.args.get('pageSize', default=Config.PageSize, type=int)
    page_index = request.args.get('pageIndex', default=Config.PageIndex, type=int)
    search_criteria = request.args.get('search_criteria')
    user = get_req_user(request)
    super_admin = user.get('superAdmin')
    user_id = user.get('id')
    if super_admin != 1:
        temp = json.loads(search_criteria)
        print(temp)
        temp['user_id'] = {"value": user_id, "operator": "eq"}
        search_criteria = json.dumps(temp)

    print(search_criteria)

    return ai_chat_impl.api_query_list_page_impl(page_size, page_index, search_criteria)


def api_find_talk_name(request):
    talk_id = int(request.args.get('talk_id'))
    return ai_chat_impl.api_find_talk_name(talk_id)


def api_find_talk_recommend(request):
    talk_id = int(request.args.get('talk_id'))
    return ai_chat_impl.api_find_talk_recommend(talk_id)


def api_del_chat(request):
    request_data = request.get_json()
    if request_data.get("id") is None:
        return ReturnTool.ErrorReturn("id为空")
    id_c = request_data.get("id")
    return ai_chat_impl.api_del_chat_impl(id_c)


def share_chat(request):
    request_data = request.get_json()
    return ai_chat_impl.share_chat_impl(request_data)


def get_redis_chat(request):
    r_id = request.args.get('r_id')
    return ai_chat_impl.get_redis_chat(r_id)
