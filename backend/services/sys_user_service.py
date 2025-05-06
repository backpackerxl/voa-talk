from services.impl import sys_user_impl

from utils import ReturnTool

from utils import Config
from utils.JwtUtils import JWTHandler


def api_sys_user_find_list_page_service(request):
    page_size = request.args.get('pageSize', default=Config.PageSize, type=int)
    page_index = request.args.get('pageIndex', default=Config.PageIndex, type=int)
    search_criteria = request.args.get('search_criteria')
    return sys_user_impl.api_sys_user_find_list_page_impl(page_size, page_index, search_criteria)


def api_sys_user_delete_ids_service(request):
    request_data = request.get_json()
    if request_data.get("id") is None:
        return ReturnTool.ErrorReturn("id为空")
    ids = request_data.get("id")
    return sys_user_impl.api_sys_user_delete_ids_impl(ids)


def api_sys_user_save_or_update_service(request):
    request_data = request.get_json()
    return sys_user_impl.api_sys_user_save_or_update_impl(request_data)


def enroll_service(request):
    """
    用户注册服务
    """
    data = request.get_json()
    name = data.get("name")
    username = data.get("username")
    email = data.get("email")
    return sys_user_impl.enroll_impl(name, username, email)


def forget_pwd_service(request):
    """
    用户找回密码服务
    """
    data = request.get_json()
    email = data.get("email")
    req_url = data.get("req_url")

    return sys_user_impl.forget_pwd_impl(email, req_url)


def reset_pwd(request):
    '''
    用户重置密码
    '''
    data = request.get_json()
    pwd = data.get('pwd')
    secret_key = data.get('secret_key')
    return sys_user_impl.reset_pwd(pwd, secret_key)


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
    # 从 payload 中获取用户名称
    # user_id = payload.get("id")
    # nick_name = payload.get("nickName")
    # super_admin = payload.get("superAdmin")
    return payload

def api_user_update_nickname(request):
    data = request.get_json()
    id = get_req_user(request).get('id')
    avatar = data.get('avatar')
    nick_name = data.get('nick_name')
    return sys_user_impl.api_user_update_nickname(id, avatar, nick_name)