import datetime
import json
import uuid

from sqlalchemy import or_

from dbinfo import DatabaseSession
from entity import SysUser
from utils import ReturnTool, Tools
from utils.JwtUtils import JWTHandler, real_ip_decorator
from utils.RedisUtils import RedisHandler
from utils.encryptUtils import aes_decrypt


@real_ip_decorator
def login_impl(request, client_ip):
    with DatabaseSession() as session:
        username = request.get_json().get("userName")
        queue = session.query(SysUser).filter(
            or_(
                SysUser.user_name == username,
                SysUser.email == username,
            )
        ).first()

        # 如果用户不存在
        if not queue:
            return ReturnTool.ErrorReturn("用户不存在")
        if queue.user_state != 1:
            return ReturnTool.ErrorReturn("用户已经停用，请联系管理员！")
        pwd = request.get_json().get('passWord')
        platform = request.get_json().get('platform')
        decrypt = aes_decrypt(pwd)
        password = Tools.verify_password(decrypt, queue.salt)

        # 检查密码是否正确，用于开发检查
        # print(f"解密后的密码: {decrypt}")
        # print(f"用户输入：{password}")
        # print(f"数据库存储：{queue.pass_word}")
        if password != queue.pass_word:
            return ReturnTool.ErrorReturn("用户名或密码错误")
        # 设置用户最后登录时间
        queue.last_login_time = datetime.datetime.now()
        session.commit()
        # 准备返回数据
        user_data = {
            "id": queue.id,
            "userName": queue.user_name,
            "nickName": queue.nick_name,
            "avatar": queue.avatar,
            "email": queue.email,
            "loginType": "voatalk",
            "IP": client_ip,
            "superAdmin": queue.super_admin,
            "bindQQ": (1 if queue.qq_open_id is None else 3),
            "bindGithub": (1 if queue.github_open_id is None else 3),
        }
        # 生成token
        token = JWTHandler().encode_jwt(user_data)
        user_data["jwtToken"] = token
        user_data["refreshToken"] = token
        user_data['exp'] = user_data['exp'].strftime("%Y-%m-%d %H:%M:%S")
        next_id = str(uuid.uuid4())
        ## 缓存登录信息
        RedisHandler().save_key("user:info:" + next_id, json.dumps(user_data), 300)  # 登录成功信息5分钟内有效
        if platform == 'mobile':
            register_authenticated = bool(queue.credentials_data_mobile)
        else:
            register_authenticated = bool(queue.credentials_data)
        return ReturnTool.SuccessReturn({
            'next_id': next_id,
            'username': queue.user_name,
            "avatar": queue.avatar,
            "platform": platform,
            'register_authenticated': register_authenticated
        })
