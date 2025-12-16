from services.impl import two_auth_impl


def register_begin(request):
    return two_auth_impl.register_begin(request)


def register_complete(request):
    return two_auth_impl.register_complete(request)


def generate_otp_qrcode(username):
    return two_auth_impl.generate_otp_qrcode(username)


def login_begin(request):
    return two_auth_impl.login_begin(request)


def login_complete(request):
    return two_auth_impl.login_complete(request)


def verify_otp(request):
    return two_auth_impl.verify_otp(request)


def verify_recovery(request):
    return two_auth_impl.verify_recovery(request)
