import traceback

from flask import Blueprint, request, jsonify

from services import sys_report_service
from utils import logs
from utils.BusinessException import BusinessException
from utils.JwtUtils import token_required
from utils.ReturnTool import ErrorReturn

sys_user_blueprint = Blueprint('report', __name__, url_prefix='/report')


@sys_user_blueprint.route('/header_data', methods=['GET'])
@token_required
def header_data():
    try:
        response = sys_report_service.header_data()
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@sys_user_blueprint.route('/top_talk', methods=['GET'])
@token_required
def top_talk():
    try:
        response = sys_report_service.top_talk()
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@sys_user_blueprint.route('/bar_talks', methods=['GET'])
@token_required
def bar_talks():
    try:
        response = sys_report_service.bar_talks(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@sys_user_blueprint.route('/model_talks', methods=['GET'])
@token_required
def model_talks():
    try:
        response = sys_report_service.model_talks(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@sys_user_blueprint.route('/line_tokens', methods=['GET'])
@token_required
def line_tokens():
    try:
        response = sys_report_service.line_tokens(request)
        return jsonify(response)
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        print(traceback.format_exc())
        logs.setup_logger().error(f'处理请求时出错: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500
