from services.impl import LoginImp
from utils.ReturnTool import ErrorReturn


def login_service(request):
    data = request.get_json()
    if len(data) == 0:
        return ErrorReturn("参数不能为空")

    return LoginImp.login_impl(request)
