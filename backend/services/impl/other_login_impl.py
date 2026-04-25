import datetime
import json
import os
from urllib.parse import unquote

import requests
from sqlalchemy import and_
from ua_parser import user_agent_parser

from dbinfo import DatabaseSession
from entity import SysUser, SysUsersLoginLogs
from utils import DbTools, Config
from utils import ReturnTool
from utils import TimeToolClass
from utils import Tools
from utils.JwtUtils import JWTHandler
from utils.RedisUtils import RedisHandler


def public_login_handler(request, queue, login_type, ip, bind_other_account):
    # 1. 获取请求头里的 User-Agent
    ua_string = request.headers.get('User-Agent', '')
    # 2. 解析设备信息
    parsed = user_agent_parser.Parse(ua_string)
    device = parsed.get('device', {})
    # 3. 拼接设备名称（最精准）
    device_model = device.get('model', '')  # 型号：iPhone 16 Pro
    if device_model is None:
        device_model = '网页登录'
    # 准备返回数据
    user_data = {
        "id": queue.id,
        "userName": queue.user_name,
        "nickName": queue.nick_name,
        "avatar": queue.avatar,
        "email": queue.email,
        "loginType": login_type,
        "IP": ip,
        "superAdmin": queue.super_admin,
        "bindQQ": 0,
        "bindGithub": 0,
    }
    # 生成token
    with DatabaseSession() as session:
        login_quen = session.query(SysUsersLoginLogs).filter(
            and_(
                SysUsersLoginLogs.name == device_model,
                SysUsersLoginLogs.user_id == queue.id
            )
        ).first()
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
                'ip': ip,
                'create_date': now,
                'user_id': queue.id
            }
            DbTools.saveOrUpdate(session, login_logs, SysUsersLoginLogs)

        # 生成token
        token = JWTHandler().encode_jwt(user_data)
        user_data["jwtToken"] = token
        user_data["refreshToken"] = refresh_id
        if bind_other_account != '':
            RedisHandler().save_key(bind_other_account, token, 300)  # 登录成功信息5分钟内有效
            return None
        return user_data


def qq(request, code, redirect_uri, ip, bind_other_account):
    client_id = "102796804"
    token_open_id = requests.get("https://graph.qq.com/oauth2.0/token", {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": os.getenv("QQ_CLIENT_SECRET"),
        "code": code,
        "redirect_uri": redirect_uri,
        "fmt": "json",
        "need_openid": 1
    })

    obj = token_open_id.json()
    if "error" in obj:
        return ReturnTool.ErrorReturn(obj["error_description"])
    access_token = obj["access_token"]
    openid = obj["openid"]
    # 如果平台已经有了次qq用户，直接登录返回
    with DatabaseSession() as session:
        queue = session.query(SysUser).filter(SysUser.qq_open_id == openid).first()
        if queue is not None:
            if queue.user_state != 1:
                return ReturnTool.ErrorReturn("QQ用户已经停用，请联系管理员！")
            # 设置用户最后登录时间
            queue.last_login_time = datetime.datetime.now()
            session.commit()
            return ReturnTool.SuccessReturn(public_login_handler(request, queue, 'qq', ip, bind_other_account))
        # 平台没有该用户，则创建用户，登录返回
        qq_user_info = requests.get("https://graph.qq.com/user/get_user_info", {
            "access_token": access_token,
            "oauth_consumer_key": client_id,
            "openid": openid,
        })
        qq_user = qq_user_info.json()
        password = Tools.generate_random_password()
        hashed_password, salt = Tools.generate_hashed_password(password)
        sql_data = {
            "nick_name": qq_user["nickname"],
            "avatar": qq_user["figureurl_2"],
            "super_admin": 0, "user_state": 1,
            "user_name": f"qq_{Tools.generate_custom_id(12)}",
            "pass_word": hashed_password,
            "salt": salt,
            "update_date": TimeToolClass.get_time(),
            "create_date": TimeToolClass.get_time(),
            "qq_open_id": openid,
        }
        DbTools.saveOrUpdate(session, sql_data, SysUser)
        queue_qq = session.query(SysUser).filter(SysUser.qq_open_id == openid).first()
        queue_qq.last_login_time = datetime.datetime.now()
        session.commit()
        return ReturnTool.SuccessReturn(public_login_handler(request, queue_qq, 'qq', ip, bind_other_account))


def github(request, code, redirect_uri, ip, bind_other_account):
    client_id = "Ov23liTrl7t8g4EZP3j7"
    github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")
    redirect_uri = unquote(redirect_uri)
    # print(code, redirect_uri, client_id, github_client_secret)
    url = "https://github.com/login/oauth/access_token"

    payload = json.dumps({
        "code": code,
        "client_id": client_id,
        "client_secret": github_client_secret,
        "redirect_uri": redirect_uri
    })
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    token_open = requests.request("POST", url, headers=headers, data=payload)
    # print(token_open)
    obj = token_open.json()
    access_token = obj["access_token"]
    if access_token is None:
        return ReturnTool.ErrorReturn("Github授权失败！", 401)
    token_type = obj["token_type"]
    user_resp = requests.get("https://api.github.com/user", headers={
        "Authorization": token_type.title() + " " + access_token
    })
    user_obj = user_resp.json()
    openid = user_obj["id"]
    username = user_obj["login"]
    avatar = user_obj["avatar_url"]
    if openid is None:
        return ReturnTool.ErrorReturn("Github授权失败！", 401)

    # 如果平台已经有了次qq用户，直接登录返回
    with DatabaseSession() as session:
        queue = session.query(SysUser).filter(SysUser.github_open_id == openid).first()
        if queue is not None:
            if queue.user_state != 1:
                return ReturnTool.ErrorReturn("github用户已经停用，请联系管理员！")
            # 设置用户最后登录时间
            queue.last_login_time = datetime.datetime.now()
            session.commit()
            return ReturnTool.SuccessReturn(public_login_handler(request, queue, 'github', ip, bind_other_account))
        # 平台没有该用户，则创建用户，登录返回
        password = Tools.generate_random_password()
        hashed_password, salt = Tools.generate_hashed_password(password)
        sql_data = {
            "nick_name": username,
            "avatar": avatar,
            "super_admin": 0, "user_state": 1,
            "user_name": f"github_{Tools.generate_custom_id(12)}",
            "pass_word": hashed_password,
            "salt": salt,
            "update_date": TimeToolClass.get_time(),
            "create_date": TimeToolClass.get_time(),
            "github_open_id": openid,
        }
        DbTools.saveOrUpdate(session, sql_data, SysUser)
        queue_github = session.query(SysUser).filter(SysUser.github_open_id == openid).first()
        queue_github.last_login_time = datetime.datetime.now()
        session.commit()
        return ReturnTool.SuccessReturn(public_login_handler(request, queue_github, 'github', ip, bind_other_account))
