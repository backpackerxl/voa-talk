import requests
import datetime

from dbinfo import DatabaseSession
from entity import SysUser
from utils import ReturnTool
from utils import TimeToolClass
from utils import Tools
from utils import DbTools
from utils.JwtUtils import JWTHandler


def public_login_handler(queue, ip):
    # 准备返回数据
    user_data = {
        "id": queue.id,
        "userName": queue.user_name,
        "nickName": queue.nick_name,
        "avatar": queue.avatar,
        "email": queue.email,
        "IP": ip,
        "superAdmin": queue.super_admin
    }
    # 生成token
    token = JWTHandler().encode_jwt(user_data)
    user_data["jwtToken"] = token
    user_data["refreshToken"] = token
    return user_data


def qq(code, redirect_uri, ip):
    client_id = "102796804"
    token_open_id = requests.get("https://graph.qq.com/oauth2.0/token", {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": "86pMgkYAZicJl14u",
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
            # 设置用户最后登录时间
            queue.last_login_time = datetime.datetime.now()
            session.commit()
            return ReturnTool.SuccessReturn(public_login_handler(queue, ip))
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
        return ReturnTool.SuccessReturn(public_login_handler(queue_qq, ip))
