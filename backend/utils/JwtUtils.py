import datetime

import jwt

from utils import Config
from functools import wraps

from flask import request, jsonify

from utils import logs


# JWT 处理器
class JWTHandler:
    def __init__(self, secret_key=Config.SecretKey, algorithm='HS256'):
        # 初始化，设置密钥和算法
        self.secret_key = secret_key
        self.algorithm = algorithm

    def encode_jwt(self, payload):
        """
        编码 JWT。 生成Token
        参数：
            payload (字典): 要包含在 JWT 中的负载
        返回值：
            字符串: 编码后的 JWT
        """
        # 在负载中添加一个 "exp"（过期时间）字段，设置过期时间为 1 天后
        payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=Config.TheExpirationTimeOfTheToken)

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_jwt(self, encoded_jwt):
        """
        解码 JWT。
        参数：
            encoded_jwt (字符串): 编码后的 JWT

        返回值：
            字典: 解码后的负载
        """
        try:
            return {
                "status": "成功",
                "code": 200,
                "data": jwt.decode(encoded_jwt, self.secret_key, algorithms=[self.algorithm]),
                "message": "验证通过"
            }

        except jwt.ExpiredSignatureError:
            return {
                "status": "失败",
                "code": 666,
                "message": "过期令牌"
            }
        except jwt.InvalidTokenError:
            return {
                "status": "失败",
                "code": 666,
                "message": "非法令牌"
            }

    # 验证Token
    def VerifyToken(self, token):
        """

        :param token:  Token
        :return: 元祖，第一个参数为布尔值，第二个参数为字典
        """
        my_jwt_handler = JWTHandler(secret_key=self.secret_key)
        decoded_payload = my_jwt_handler.decode_jwt(token)
        if decoded_payload['code'] == 200:
            # session = DBSession()
            # userData = session.query(UserModel).filter(UserModel.id == decoded_payload['data']['id']).one()
            # session.close()
            # if userData.token != token:
            #     return False, {
            #         "status": "失败",
            #         "code": 666,
            #         "message": "非法令牌"
            #     }
            return True, decoded_payload['data']
        else:
            raise ValueError(decoded_payload.get("message"))  # 抛出异常token 无效


# 定义一个装饰器函数

"""
装饰器类，用于验证 token。
还可以添加其它的函数，比如验证用户是否有权限访问某个路由。
"""


def token_required(f):
    # wraps 用于保留被装饰函数的名称和文档字符串
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从请求头中获取 token
        token = request.headers.get('token')

        # 如果请求头中没有 token，则返回 401 未授权错误
        if not token:
            return jsonify({"message": "缺少令牌", "code": 401}), 401

        # 尝试验证 token
        try:
            # 创建 JWTHandler 实例
            jwt_handler = JWTHandler()
            # 使用 JWTHandler 的 VerifyToken 方法验证 token
            valid, payload = jwt_handler.VerifyToken(token)
            # 如果 token 无效，抛出 ValueError 异常
            if not valid:
                raise ValueError("无效的令牌")
            # 从 payload 中获取用户名称
            user_name = payload.get("userName")
            nickName = payload.get("nickName")
            admin = payload.get("superAdmin")
            # 获取请求的 IP 地址
            ip_address = request.remote_addr
            # 获取访问的模块（路由）
            accessed_module = request.endpoint
            # 记录日志到数据库
            logs.setup_logger().info(f"{nickName}请求了后端，使用的IP为：{ip_address}，请求的方法为：{accessed_module}")
            if admin == 0:
                return jsonify({"message": "普通用户，无权调用", "code": 403}), 403
        # 捕获 ValueError 异常，并返回 401 未授权错误
        except ValueError as e:
            return jsonify({"message": str(e), "code": 401}), 401

        # 如果 token 验证通过，则执行原始函数
        return f(*args, **kwargs)

    # 返回装饰后的函数
    return decorated_function


def token_on(f):
    # wraps 用于保留被装饰函数的名称和文档字符串
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从请求头中获取 token
        token = request.headers.get('token')

        # 如果请求头中没有 token，则返回 401 未授权错误
        if not token:
            return jsonify({"message": "缺少令牌", "code": 401}), 401

        # 尝试验证 token
        try:
            # 创建 JWTHandler 实例
            jwt_handler = JWTHandler()
            # 使用 JWTHandler 的 VerifyToken 方法验证 token
            valid, payload = jwt_handler.VerifyToken(token)
            # 如果 token 无效，抛出 ValueError 异常
            if not valid:
                raise ValueError("无效的令牌")
            # 从 payload 中获取用户名称
            nickName = payload.get("nickName")
            # 获取请求的 IP 地址
            ip_address = request.remote_addr
            # 获取访问的模块（路由）
            accessed_module = request.endpoint
            # 记录日志到数据库
            logs.setup_logger().info(f"{nickName}请求了后端，使用的IP为：{ip_address}，请求的方法为：{accessed_module}")
        # 捕获 ValueError 异常，并返回 401 未授权错误
        except ValueError as e:
            return jsonify({"message": str(e), "code": 401}), 401

        # 如果 token 验证通过，则执行原始函数
        return f(*args, **kwargs)

    # 返回装饰后的函数
    return decorated_function


def add_update_time(func):
    """
    添加更新时间
    :param func:  是POST请求并且请求体是JSON数据，会在update_time字段添加当前时间
    :return:
    """
    from datetime import datetime

    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method == 'POST':
            data = request.get_json()  # 获取请求的JSON数据
            if isinstance(data, dict):  # 确保数据是字典格式
                data['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return func(*args, **kwargs)

    return wrapper
