from flask import Blueprint, request, jsonify
import traceback
from services import model_config_service
from utils import logs
from utils.BusinessException import BusinessException
from utils.JwtUtils import token_required, add_update_time, token_on
from utils.ReturnTool import ErrorReturn

model_config_blueprint = Blueprint('model_config', __name__, url_prefix='/model_config')


@model_config_blueprint.route('/query', methods=['GET'])
@token_required
def api_find_list_page():
    try:
        response = model_config_service.api_query_page_service(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500

@model_config_blueprint.route('/list', methods=['GET'])
@token_on
def api_list_page():
    try:
        response = model_config_service.api_list_page(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@model_config_blueprint.route('/delete', methods=['POST'])
@token_required
def api_delete_ids():
    try:
        response = model_config_service.api_delete_ids_service(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@model_config_blueprint.route('/saveOrUpdate', methods=['POST'])
@token_required
@add_update_time
def api_save_or_update():
    try:
        response = model_config_service.api_save_or_update_service(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


