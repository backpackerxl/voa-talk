import traceback

from flask import jsonify, request, Blueprint

from services import ai_chat_service
from utils import logs
from utils.BusinessException import BusinessException
from utils.JwtUtils import token_on
from utils.ReturnTool import ErrorReturn

ai_chat_blueprint = Blueprint('ai_chat', __name__, url_prefix='/ai_chat')


@ai_chat_blueprint.route('/stream', methods=['POST'])
@token_on
def dialogue():
    try:
        response = ai_chat_service.ai_chat_dialogue_serve(request)
        return response  # 直接返回 Response 对象用于流式传输
    except BusinessException as e:
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        print(traceback.format_exc())
        logs.setup_logger().error(f'处理请求时出错: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@ai_chat_blueprint.route('/save_chat', methods=['POST'])
@token_on
def save_chat():
    try:
        response = ai_chat_service.ai_save_chat_serve(request)
        return response  # 直接返回 Response 对象用于流式传输
    except BusinessException as e:
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        print(traceback.format_exc())
        logs.setup_logger().error(f'处理请求时出错: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@ai_chat_blueprint.route('/save_chat_title', methods=['POST'])
@token_on
def save_chat_title():
    try:
        response = ai_chat_service.save_chat_title(request)
        return response  # 直接返回 Response 对象用于流式传输
    except BusinessException as e:
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        print(traceback.format_exc())
        logs.setup_logger().error(f'处理请求时出错: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@ai_chat_blueprint.route('/list', methods=['GET'])
@token_on
def api_list_page():
    try:
        response = ai_chat_service.api_list_page(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@ai_chat_blueprint.route('/one_chat', methods=['GET'])
@token_on
def one_chat():
    try:
        response = ai_chat_service.one_chat(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@ai_chat_blueprint.route('/delete', methods=['POST'])
@token_on
def api_delete_ids():
    try:
        response = ai_chat_service.api_delete_ids_service(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@ai_chat_blueprint.route('/update', methods=['POST'])
@token_on
def api_update_ids():
    try:
        response = ai_chat_service.api_update_ids(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@ai_chat_blueprint.route('/query', methods=['GET'])
@token_on
def api_find_list_page():
    try:
        response = ai_chat_service.api_query_page_service(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@ai_chat_blueprint.route('/queryTalkName', methods=['GET'])
@token_on
def api_find_talk_name():
    try:
        response = ai_chat_service.api_find_talk_name(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500


@ai_chat_blueprint.route('/queryRecommend', methods=['GET'])
@token_on
def api_find_talk_recommend():
    try:
        response = ai_chat_service.api_find_talk_recommend(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500

@ai_chat_blueprint.route('/delOneChat', methods=['POST'])
@token_on
def api_del_chat():
    try:
        response = ai_chat_service.api_del_chat(request)
        return jsonify(response), response.get("code")
    except BusinessException as e:
        # 特定的业务逻辑异常处理
        print(traceback.format_exc())
        logs.setup_logger().error(f"业务错误: {str(e)}")
        return jsonify(ErrorReturn(str(e), e.error_code))
    except Exception as e:
        logs.setup_logger().error(f'Error processing request: {e}')
        return jsonify(ErrorReturn(f"内部错误：{e}", 500)), 500
