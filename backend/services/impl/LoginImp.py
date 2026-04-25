import datetime
import json
import uuid

from sqlalchemy import or_, and_
from ua_parser import user_agent_parser

from dbinfo import DatabaseSession
from entity import SysUser, SysUserWebAuth, SysUsersLoginLogs
from utils import ReturnTool, Tools, DbTools, Config
from utils.JwtUtils import JWTHandler, real_ip_decorator
from utils.RedisUtils import RedisHandler
from utils.encryptUtils import aes_decrypt


@real_ip_decorator
def login_impl(request, client_ip):
    with DatabaseSession() as session:
        username = request.get_json().get("userName")
        # 1. 获取请求头里的 User-Agent
        ua_string = request.headers.get('User-Agent', '')
        # 2. 解析设备信息
        parsed = user_agent_parser.Parse(ua_string)
        device = parsed.get('device', {})
        # 3. 拼接设备名称（最精准）
        device_model = device.get('model', '')  # 型号：iPhone 16 Pro
        if device_model is None:
            device_model = '网页登录'

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
        login_quen = session.query(SysUsersLoginLogs).filter(
            and_(
                SysUsersLoginLogs.name == device_model,
                SysUsersLoginLogs.user_id == queue.id
            )
        ).first()
        if login_quen is None:
            refresh_token = JWTHandler().encode_jwt(user_data, Config.ReExpirationTimeOfTheToken)
            refresh_id = Tools.generate_custom_id(15)

            now = datetime.datetime.now()
            login_logs = {
                'refresh_id': refresh_id,
                'name': device_model,
                'refresh_token': refresh_token,
                'ip': client_ip,
                'create_date': now,
                'user_id': queue.id
            }
            DbTools.saveOrUpdate(session, login_logs, SysUsersLoginLogs)
        else:
            resp = JWTHandler().decode_jwt(login_quen.refresh_token)
            refresh_id = login_quen.refresh_id
            if resp['code'] != 200:
                refresh_token = JWTHandler().encode_jwt(user_data, Config.ReExpirationTimeOfTheToken)
                refresh_id = Tools.generate_custom_id(15)

                now = datetime.datetime.now()
                login_logs = {
                    'refresh_id': refresh_id,
                    'name': device_model,
                    'refresh_token': refresh_token,
                    'ip': client_ip,
                    'create_date': now,
                    'user_id': queue.id
                }
                DbTools.saveOrUpdate(session, login_logs, SysUsersLoginLogs)

        token = JWTHandler().encode_jwt(user_data)
        user_data["jwtToken"] = token
        user_data["refreshToken"] = refresh_id
        next_id = str(uuid.uuid4())
        ## 缓存登录信息
        RedisHandler().save_key("user:info:" + next_id, json.dumps(user_data), 300)  # 登录成功信息5分钟内有效
        c_queue_opt = session.query(SysUserWebAuth.content).filter(and_(
            SysUserWebAuth.type == '1',  # 是否已经注册二次认证
            SysUserWebAuth.user_id == queue.id
        )).first()

        return ReturnTool.SuccessReturn({
            'next_id': next_id,
            'username': queue.user_name,
            "avatar": queue.avatar,
            "platform": platform,
            'register_authenticated': bool(c_queue_opt)
        })
