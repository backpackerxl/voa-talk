from flask import jsonify, request, Blueprint

from services import two_auth_service
from utils import logs
from utils.ReturnTool import ErrorReturn

two_auth_blueprint = Blueprint('two_auth', __name__, url_prefix='/two_auth')


@two_auth_blueprint.route('/qr/<username>')
def show_qr(username):
    try:
        response = two_auth_service.show_qr(username)
        return jsonify(response)
    except Exception as e:
        logs.setup_logger().error(f"Show QR Code error: {str(e)}")
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


# 1. 注册 - 生成注册选项
@two_auth_blueprint.route('/register/begin', methods=['POST'])
def register_begin():
    try:
        response = two_auth_service.register_begin(request)
        return jsonify(response)
    except Exception as e:
        import traceback
        logs.setup_logger().error(f"Registration begin error: {str(e)}")
        logs.setup_logger().error(f"Full traceback: {traceback.format_exc()}")
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


# 2. 注册 - 验证注册响应
@two_auth_blueprint.route('/register/complete', methods=['POST'])
def register_complete():
    try:
        response = two_auth_service.register_complete(request)
        return jsonify(response)
    except Exception as e:
        logs.setup_logger().error(f"Registration complete error: {str(e)}")
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


# 生成OTP QR码
@two_auth_blueprint.route('/otp/qrcode/<username>', methods=['GET'])
def generate_otp_qrcode(username):
    try:
        response = two_auth_service.generate_otp_qrcode(username)
        return jsonify(response)
    except Exception as e:
        logs.setup_logger().error(f"Generate OTP QR Code error: {str(e)}")
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


# 3. 登录 - 生成认证选项
@two_auth_blueprint.route('/login/begin', methods=['POST'])
def login_begin():
    try:
        response = two_auth_service.login_begin(request)
        return jsonify(response)
    except Exception as e:
        import traceback
        logs.setup_logger().error(f"Login begin error: {str(e)}")
        logs.setup_logger().error(f"Full traceback: {traceback.format_exc()}")
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


# 4. 登录 - 验证认证响应
@two_auth_blueprint.route('/login/complete', methods=['POST'])
def login_complete():
    try:
        response = two_auth_service.login_complete(request)
        return jsonify(response)
    except Exception as e:
        logs.setup_logger().error(f"Login complete error: {str(e)}")
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


# 5. OTP验证接口
@two_auth_blueprint.route('/otp/verify', methods=['POST'])
def verify_otp():
    try:
        response = two_auth_service.verify_otp(request)
        return jsonify(response)
    except Exception as e:
        logs.setup_logger().error(f"OTP verification error: {str(e)}")
        return jsonify({'error': str(e)}), 400
