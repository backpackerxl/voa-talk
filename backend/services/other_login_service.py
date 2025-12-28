from services.impl import other_login_impl


def other_login(request):
    data = request.get_json()
    code = data.get("code")
    redirect_uri = data.get("redirect_uri")
    login_type = data.get("login_type")
    bind_other_account = data.get("bind_other_account")
    ip = request.remote_addr
    if login_type == 'qqLogin':
        return other_login_impl.qq(code, redirect_uri, ip, bind_other_account)
    elif login_type == 'githubLogin':
        return other_login_impl.github(code, redirect_uri, ip, bind_other_account)
    else:
        return None
