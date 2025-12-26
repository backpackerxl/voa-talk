import traceback

from flask import jsonify, request, Blueprint

from services import loginService, other_login_service
from utils import logs
from utils.BusinessException import BusinessException
from utils.ReturnTool import ErrorReturn

login_blueprint = Blueprint('login', __name__, url_prefix='/login')


# 登录
@login_blueprint.route('/pt_login', methods=['POST'])
def pt_login():
    try:
        response = loginService.login_service(request)
        return jsonify(response)
    except BusinessException as e:
        # 特定的业务逻辑异常
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"code": 500, "msg": f"服务器内部错误: {str(e)}"}), 500


@login_blueprint.route("/other_login", methods=["POST"])
def other_login():
    try:
        response = other_login_service.other_login(request)
        if response is None:
            return jsonify(ErrorReturn("不支持的第三方登录！", 404)), 404
        return jsonify(response), response.get("code")
    except BusinessException as e:
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        print(traceback.format_exc())
        logs.setup_logger().error(f'处理请求时出错: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500
