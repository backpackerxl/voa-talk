import traceback

from flask import jsonify, request, Blueprint

from services.loginService import login_service
from utils import logs
from utils.BusinessException import BusinessException
from utils.ReturnTool import ErrorReturn

login_blueprint = Blueprint('login', __name__, url_prefix='/login')

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
