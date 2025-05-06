import traceback

from flask import jsonify, request, Blueprint

from services import loginService
from services.loginService import getverifycode_service, login_service
from utils import logs
from utils.BusinessException import BusinessException
from utils.ReturnTool import ErrorReturn

login_blueprint = Blueprint('login', __name__, url_prefix='/login')


# 获取验证码
@login_blueprint.route('/getVerifyCode', methods=['GET'])
def getverifycode():
    try:
        response = getverifycode_service(request)
        return jsonify(response)
    except BusinessException as e:
        # 特定的业务逻辑异常
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))

    except Exception as e:
        print(traceback.format_exc())

        return jsonify({"code": 500, "msg": f"服务器内部错误: {str(e)}"}), 500


# 登录
@login_blueprint.route('/login', methods=['POST'])
def login():
    try:
        response = login_service(request)
        return jsonify(response)
    except BusinessException as e:
        # 特定的业务逻辑异常
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"code": 500, "msg": f"服务器内部错误: {str(e)}"}), 500


@login_blueprint.route('/retrievePassword', methods=['POST'])
def retrieve_password_blueprint():
    try:
        response = loginService.retrieve_password_servie(request)
        return jsonify(response)
    except BusinessException as e:
        # 特定的业务逻辑异常
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"code": 500, "msg": f"服务器内部错误: {str(e)}"}), 500


@login_blueprint.route('/getTheEmailVerificationCode', methods=['POST'])
def get_the_email_verification_code():
    """
    获取邮箱验证码
    :return:
    """
    try:
        response = loginService.get_the_email_verification_code_servie(request)
        return jsonify(response)
    except BusinessException as e:
        # 特定的业务逻辑异常
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"code": 500, "msg": f"服务器内部错误: {str(e)}"}), 500
