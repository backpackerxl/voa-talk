import traceback

from flask import Blueprint, request, jsonify

from services import sys_user_service
from utils import logs
from utils.BusinessException import BusinessException
from utils.JwtUtils import token_required, add_update_time, token_on
from utils.ReturnTool import ErrorReturn

sys_user_blueprint = Blueprint('sys_user', __name__, url_prefix='/sys_user')


@sys_user_blueprint.route('/findListPage', methods=['GET'])
@token_required
def api_find_list_page():
    try:
        response = sys_user_service.api_sys_user_find_list_page_service(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@sys_user_blueprint.route('/delete', methods=['POST'])
@token_required
def api_delete_ids():
    try:
        response = sys_user_service.api_sys_user_delete_ids_service(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@sys_user_blueprint.route('/saveOrUpdate', methods=['POST'])
@token_required
@add_update_time
def api_save_or_update():
    try:
        response = sys_user_service.api_sys_user_save_or_update_service(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@sys_user_blueprint.route('/updateUser', methods=['POST'])
@token_on
@add_update_time
def api_user_update_nickname():
    try:
        response = sys_user_service.api_user_update_nickname(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@sys_user_blueprint.route('/enroll', methods=['POST'])
@add_update_time
def enroll():
    try:
        response = sys_user_service.enroll_service(request)
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


@sys_user_blueprint.route('/forgetPwd', methods=['POST'])
@add_update_time
def forget_pwd():
    try:
        response = sys_user_service.forget_pwd_service(request)
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


@sys_user_blueprint.route('/resetPWD', methods=['POST'])
@add_update_time
def reset_pwd():
    try:
        response = sys_user_service.reset_pwd(request)
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
