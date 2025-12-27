from services.impl import other_login_impl


def other_login(request):
    data = request.get_json()
    code = data.get("code")
    redirect_uri = data.get("redirect_uri")
    login_type = data.get("login_type")
    ip = request.remote_addr
    if login_type == 'qqLogin':
        return other_login_impl.qq(code, redirect_uri, ip)
    elif login_type == 'githubLogin':
        return other_login_impl.github(code, ip)
    else:
        return None
