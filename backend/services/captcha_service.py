from services.impl import captcha_impl


def verify(request):
    data = request.get_json()
    token = data.get("token")
    user_x = float(data.get("x", 0))
    return captcha_impl.verify(token, user_x)


def refresh():
    return captcha_impl.refresh()
