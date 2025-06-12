import json

from services.impl import LoginImp
from utils.RedisUtils import RedisHandler
from utils.ReturnTool import ErrorReturn


# from utils.Redis import RedisHandler


def getverifycode_service(request):
    print('获取登录验证码')
    return LoginImp.getverifycode_impl()


def login_service(request):
    data = request.get_json()
    if len(data) == 0:
        return ErrorReturn("参数不能为空")
    res = RedisHandler().get_key(data["captcha_code"])
    if res is None:
        return ErrorReturn("请通过验证后，再尝试登录")

    if not json.loads(res):
        return ErrorReturn("请通过验证后，再尝试登录")

    return LoginImp.login_impl(request)


def retrieve_password_servie(request):
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')
    return LoginImp.retrieve_password_servie_servie(email, code)


def get_the_email_verification_code_servie(request):
    """
    获取邮箱验证码
    :param request:
    :return:
    """
    data = request.get_json()
    email = data.get('email')
    if email is None:
        return ErrorReturn("邮箱不能为空")
    return LoginImp.get_the_email_verification_code_servie(email)
