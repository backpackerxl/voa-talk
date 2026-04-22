import traceback

from flask import Blueprint, request, jsonify

from services import email_logs_service
from utils import logs
from utils.BusinessException import BusinessException
from utils.JwtUtils import token_required
from utils.ReturnTool import ErrorReturn

email_logs_blueprint = Blueprint('email_logs', __name__, url_prefix='/email_logs')


@email_logs_blueprint.route('/findListPage', methods=['GET'])
@token_required
def api_find_list_page():
    try:
        response = email_logs_service.api_send_email_find_list_page_service(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@email_logs_blueprint.route('/getEmailBody/<eid>', methods=['GET'])
@token_required
def api_get_email_body(eid):
    try:
        response = email_logs_service.api_get_email_body(eid)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@email_logs_blueprint.route('/findUsers', methods=['GET'])
@token_required
def api_find_users():
    try:
        response = email_logs_service.api_find_users(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@email_logs_blueprint.route('/delete', methods=['POST'])
@token_required
def api_delete_ids():
    try:
        response = email_logs_service.api_delete_ids_service(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@email_logs_blueprint.route('/sendEmail', methods=['POST'])
@token_required
def api_send_email():
    try:
        response = email_logs_service.api_send_email_service(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500
