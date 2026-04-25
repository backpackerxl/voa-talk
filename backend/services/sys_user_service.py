from services.impl import sys_user_impl
from utils import Config
from utils import ReturnTool
from utils.JwtUtils import get_req_user
from utils.RedisUtils import RedisHandler
from utils.ReturnTool import ErrorReturn


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
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    captcha_code = data.get("captcha_code")
    redis_code = RedisHandler().get_key(email)
    if redis_code is None:
        return ErrorReturn("请先获取邮箱验证码！")

    if captcha_code != redis_code:
        return ErrorReturn("邮箱验证码错误！")

    return sys_user_impl.enroll_impl(password, username, email)


def enroll_code(request):
    email = request.get_json().get("email")
    username = request.get_json().get("username")
    return sys_user_impl.enroll_code_impl(username, email)


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


@get_req_user
def send_email_code(request, req_user):
    '''
    用户获取验证码
    '''
    data = request.get_json()
    user_id = req_user.get("id")
    email = data["email"]
    nick_name = req_user.get("nickName")

    return sys_user_impl.send_email_code(user_id, email, nick_name)


@get_req_user
def update_user_email(request, req_user):
    '''
    用户重置邮箱号
    '''
    data = request.get_json()
    user_id = req_user.get('id')
    email = data["email"]
    code = data["verCode"]
    redis_code = RedisHandler().get_key("user:email:code:" + str(user_id))
    if not redis_code:
        return ReturnTool.ErrorReturn('验证码已过期！', 401)
    if code != redis_code:
        return ReturnTool.ErrorReturn('验证码错误！', 500)

    RedisHandler().remove_key("user:email:code:" + str(user_id))

    return sys_user_impl.update_user_email(email, user_id)


@get_req_user
def api_user_update_nickname(request, req_user):
    data = request.get_json()
    id = req_user.get('id')
    avatar = data.get('avatar')
    nick_name = data.get('nick_name')
    return sys_user_impl.api_user_update_nickname(id, avatar, nick_name)


def get_refresh_token(refresh_id):
    return sys_user_impl.get_refresh_token(refresh_id)


@get_req_user
def query_login_user(req_user):
    return sys_user_impl.query_login_user(req_user)


def sing_out_device(request):
    return sys_user_impl.sing_out_device(request)