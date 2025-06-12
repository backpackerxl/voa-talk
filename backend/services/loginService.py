import json

from services.impl import LoginImp
from utils.RedisUtils import RedisHandler
from utils.ReturnTool import ErrorReturn


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
