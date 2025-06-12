import traceback

from flask import jsonify, request, Blueprint

from services import captcha_service
from utils import logs
from utils.BusinessException import BusinessException
from utils.ReturnTool import ErrorReturn

captcha_blueprint = Blueprint('captcha', __name__, url_prefix='/captcha')


@captcha_blueprint.route("/verify", methods=["POST"])
def verify():
    try:
        response = captcha_service.verify(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        print(traceback.format_exc())
        logs.setup_logger().error(f'处理请求时出错: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@captcha_blueprint.route("/refresh", methods=['GET'])
def refresh():
    try:
        response = captcha_service.refresh()
        return jsonify(response), response.get("code")
    except BusinessException as e:
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        print(traceback.format_exc())
        logs.setup_logger().error(f'处理请求时出错: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500
