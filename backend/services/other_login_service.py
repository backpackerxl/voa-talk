from services.impl import other_login_impl
from utils.JwtUtils import real_ip_decorator


@real_ip_decorator
def other_login(request, client_ip):
    data = request.get_json()
    code = data.get("code")
    redirect_uri = data.get("redirect_uri")
    login_type = data.get("login_type")
    bind_other_account = data.get("bind_other_account")

    if login_type == 'qqLogin':
        return other_login_impl.qq(code, redirect_uri, client_ip, bind_other_account)
    elif login_type == 'githubLogin':
        return other_login_impl.github(code, redirect_uri, client_ip, bind_other_account)
    else:
        return None
