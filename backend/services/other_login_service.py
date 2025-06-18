from services.impl import other_login_impl


def qq(request):
    data = request.get_json()
    code = data.get("code")
    redirect_uri = data.get("redirect_uri")
    ip = request.remote_addr
    return other_login_impl.qq(code, redirect_uri, ip)
