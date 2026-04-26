import datetime
import hashlib
import json
import time

import bcrypt
from dateutil.relativedelta import relativedelta
from sqlalchemy import or_, and_

from dbinfo import DatabaseSession
from dto import SysUserDTO
from entity import SysUser, EmailLogs, SysUsersLoginLogs
from utils import DbTools, Config, Tools
from utils import ReturnTool
from utils import SendMail
from utils import TimeToolClass
from utils.GetChatId import Snowflake
from utils.JwtUtils import JWTHandler
from utils.RedisUtils import RedisHandler
from utils.encryptUtils import aes_decrypt

snowflake = Snowflake(data_center_id=1, worker_id=2)


def api_sys_user_find_list_page_impl(page_size, page_index, search_criteria):
    with DatabaseSession() as session:
        query = session.query(SysUserDTO)
        # 使用公用方法动态添加搜索条件
        query = DbTools.apply_filters(query, SysUserDTO, search_criteria)
        # 根据需要应用过滤器
        paginated_data = DbTools.find_list_page(query, page_size, page_index)
        return ReturnTool.SuccessReturn(paginated_data)


def api_sys_user_delete_ids_impl(ids):
    """
    删除用户
    """
    id_list = ids.split(',')
    with DatabaseSession() as session:
        session.query(SysUser).filter(SysUser.id.in_(id_list)).delete()
        session.commit()
        return ReturnTool.SuccessReturn()


# 验证用户输入的密码是否与存储的哈希密码匹配
def verify_password(input_password, salt):
    """
    验证用户输入的密码是否与存储的哈希密码匹配。
    :param input_password: 用户输入的密码（明文）
    :param salt: 用于哈希过程的盐值
    :return: 布尔值，表示密码是否匹配
    """

    # 将用户输入的密码和盐值结合起来
    salted_input = input_password + salt
    # 对结合后的字符串进行 SHA-256 哈希处理
    hashed_input = hashlib.sha256(salted_input.encode()).hexdigest()
    # 比较处理后的哈希值密码
    return hashed_input


def api_sys_user_save_or_update_impl(request_data):
    """
    用户新增或编辑
    """
    with DatabaseSession() as session:
        if request_data.get("pass_word") is not None:
            queue = session.query(SysUser).filter(SysUser.user_name == request_data.get("user_name")).first()
            password = verify_password(request_data.get("pass_word"), queue.salt)
            request_data['pass_word'] = password
        # 使用 saveOrUpdate 函数
        result = DbTools.saveOrUpdate(session, request_data, SysUser)
        if result:
            return ReturnTool.SuccessReturn()
        else:
            return ReturnTool.ErrorReturn('数据没有找到')


# 哈希密码
def password_hash(password):
    """
    使用bcrypt哈希密码
    :param password:
    :return:
    """
    # 使用一个固定的“盐”来哈希密码
    salt = Config.HashingPassword
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def enroll_impl(password, username, email):
    """
    用户注册服务
    :param password:
    :param username:
    :param email:
    :return:
    """
    with DatabaseSession() as session:
        # 新增用户记录
        hashed_password, salt = Tools.generate_hashed_password(aes_decrypt(password))
        sql_data = {
            'user_name': username, 'nick_name': 'VT_' + Tools.generate_random_password(5), 'email': email,
            'pass_word': hashed_password, 'salt': salt,
            "update_date": TimeToolClass.get_time(), "create_date": TimeToolClass.get_time(),
            "super_admin": 0, "user_state": 1
        }
        DbTools.saveOrUpdate(session, sql_data, SysUser)
    return ReturnTool.SuccessReturn('注册成功！')


def enroll_code_impl(username, email):
    subject = f"新用户注册"
    code_email = Tools.generate_code_email()
    body = (f'<p style="text-indent: 2em;">'
            f'<img src="data:image/png;base64,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" alt="logo" data-href="" style="width: 50.50px;height: 52.61px;"></p>'
            f'<p style="text-indent: 2em;">'
            f'<span style="color: rgb(96, 98, 102); font-size: 14px;">尊敬的用户您好：</span></p>'
            f'<p style="text-indent: 2em;"><span style="color: rgb(96, 98, 102); font-size: 14px;">您正在注册Voatalk账号，您的验证码是：{code_email}</span></p>'
            f'<p style="text-indent: 2em;"><span style="color: rgb(96, 98, 102);font-size: 14px;">上述验证码5分钟内有效，如失效，请您重新申请发送邮箱验证码进行认证。</span></p>'
            f'<p style="text-indent: 2em;">voatalk 平台项目组</p>'
            f'<p style="text-indent: 2em;">{datetime.datetime.now().strftime("%Y年%m月%d日")}</p>')
    with DatabaseSession() as session:
        user_exist = session.query(SysUser).filter(
            or_(
                SysUser.user_name == username,
                SysUser.email == email,
            )
        ).first()
        if user_exist:
            if user_exist.user_name == username:
                return ReturnTool.ErrorReturn('用户名已被注册！')
            if user_exist.email == email:
                return ReturnTool.ErrorReturn('邮箱已被注册！')
        RedisHandler().save_key(email, str(code_email), 300)  # 验证码10分钟保活
        if SendMail.send_email(email, subject, body, True) != '电子邮件发送成功！':
            return ReturnTool.ErrorReturn('邮件发送失败，请检查邮箱是否正确')
        # 保存发送记录
        now = datetime.datetime.fromtimestamp(time.time())
        request_data = {
            "subject": subject,
            "body": body,
            "send_users": json.dumps([email]),
            "create_date": now,
        }
        DbTools.saveOrUpdate(session, request_data, EmailLogs)
    return ReturnTool.SuccessReturn('邮件发送成功，注意查收！')


def forget_pwd_impl(email, req_url):
    with DatabaseSession() as session:
        user_exist = session.query(SysUser).filter_by(email=email).first()
        if user_exist:
            # 存在此用户
            subject = f"{user_exist.nick_name}重置密码"
            key = str(snowflake.next_id())
            body = (
                f'<p style="text-indent: 2em;">'
                f'<img src="data:image/png;base64,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" alt="logo" data-href="" style="width: 50.50px;height: 52.61px;"></p>'
                f'<p style="text-indent: 2em; text-align: left;">'
                f'<span style="color: rgb(19, 24, 29); font-size: 14px;">您好：</span><span style="color: rgb(19, 24, 29);'
                f' font-size: 14px;"><strong>{user_exist.nick_name}</strong></span></p><p style="text-indent: 2em; text-align: left;"><span style="color: rgb(19, 24, 29); font-size: 14px;">您的登录账号为：</span><span style="color: rgb(19, 24, 29); font-size: 14px;"><strong>bxl</strong></span>'
                f'<span style="color: rgb(19, 24, 29); font-size: 14px;">，正在执行</span><span style="color: rgb(225, 60, 57); font-size: 14px;"><strong>重置密码</strong></span><span style="color: rgb(19, 24, 29); font-size: 14px;">操作</span></p>'
                f'<p style="text-indent: 2em; text-align: left;"><span style="color: rgb(19, 24, 29); font-size: 14px;">请点击此链接：</span><a href="{req_url}/{key}" target="_blank">重置密码</a></p>'
                f'<p style="text-indent: 2em; text-align: left;"><span style="color: rgb(19, 24, 29); font-size: 14px;">注意：此链接</span><span style="color: rgb(225, 60, 57); font-size: 14px;">5分钟内有效！</span>'
                f'<span style="color: rgb(19, 24, 29); font-size: 14px;">若无此操作请忽略此邮件</span></p>'
                f'<p style="text-indent: 2em;">voatalk 平台项目组</p>'
                f'<p style="text-indent: 2em;">{datetime.datetime.now().strftime("%Y年%m月%d日")}</p>')
            if SendMail.send_email(email, subject, body, True) != '电子邮件发送成功！':
                return ReturnTool.ErrorReturn('邮件发送失败，请检查邮箱是否正确')
            else:
                RedisHandler().save_key(key, json.dumps({
                    "user_name": user_exist.user_name,
                    "email": user_exist.email,
                }), 300)  # 链接10分钟保活
                now = datetime.datetime.fromtimestamp(time.time())
                request_data = {
                    "subject": subject,
                    "body": body,
                    "send_users": json.dumps([user_exist.email]),
                    "create_date": now,
                }
                DbTools.saveOrUpdate(session, request_data, EmailLogs)
        else:
            return ReturnTool.ErrorReturn('此邮箱未注册')

    return ReturnTool.SuccessReturn()


def reset_pwd(pwd, secret_key):
    json_str = RedisHandler().get_key(secret_key)
    if json_str is None:
        return ReturnTool.ErrorReturn('重置秘钥不存在')

    user_info = json.loads(json_str)
    with DatabaseSession() as session:
        user_exist = session.query(SysUser).filter_by(email=user_info['email'],
                                                      user_name=user_info['user_name']).first()
        if user_exist:
            password = aes_decrypt(pwd)
            hashed_password, salt = Tools.generate_hashed_password(password)
            sql_data = {
                'id': user_exist.id,
                'pass_word': hashed_password,
                'salt': salt,
                "update_date": TimeToolClass.get_time()
            }
            DbTools.saveOrUpdate(session, sql_data, SysUser)
        else:
            return ReturnTool.ErrorReturn(f'{user_info.user_name}不存在')

    return ReturnTool.SuccessReturn()


def send_email_code(user_id, email, nick_name):
    code_email = Tools.generate_code_email()
    subject = nick_name + "绑定新邮箱"
    body = f"""
    <p style="text-indent: 2em;"><img src="data:image/png;base64,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" alt="logo" data-href="" style="width: 50.50px;height: 52.61px;"></p>
    <p style="text-indent: 2em;">{nick_name}，您好：</p>
    <p style="text-indent: 2em;">您正在绑定新邮箱号。</p>
    <p style="text-indent: 2em;">您的验证码为：{code_email}</p>
    <p style="text-indent: 2em;">上述验证码5分钟内有效，如失效，请您重新申请发送邮箱验证码进行认证。</p>
    <p style="text-indent: 2em;">voatalk 平台项目组</p>
    <p style="text-indent: 2em;">{datetime.datetime.now().strftime("%Y年%m月%d日")}</p>
    """
    if SendMail.send_email(email, subject, body, True) != '电子邮件发送成功！':
        return ReturnTool.ErrorReturn('邮件发送失败，请检查邮箱是否正确')
    else:
        RedisHandler().save_key("user:email:code:" + str(user_id), str(code_email), 300)  # 链接10分钟保活
        with DatabaseSession() as session:
            now = datetime.datetime.fromtimestamp(time.time())
            request_data = {
                "subject": subject,
                "body": body,
                "send_users": json.dumps([email]),
                "create_date": now,
            }
            DbTools.saveOrUpdate(session, request_data, EmailLogs)
    return ReturnTool.SuccessReturn()


def update_user_email(email, user_id):
    with DatabaseSession() as session:
        queue = session.query(SysUser).filter(SysUser.id == user_id).first()
        email_queue = session.query(SysUser).filter(SysUser.email == email).first()
        if email_queue:
            return ReturnTool.ErrorReturn("此邮箱已注册，可以通过邮箱找回密码！")

        if not queue:
            return ReturnTool.ErrorReturn("用户未注册！")
        sql_data = {
            'id': queue.id,
            'email': email,
            'otp_secrets': None,
            'credentials_data': None,
            'recovery_code_md5': None,
            "update_date": TimeToolClass.get_time()
        }
        # 使用 saveOrUpdate 函数
        result = DbTools.saveOrUpdate(session, sql_data, SysUser)
        if result:
            return ReturnTool.SuccessReturn()
        else:
            return ReturnTool.ErrorReturn('修改失败！')


def api_user_update_nickname(id, avatar, nick_name):
    with DatabaseSession() as session:
        queue = session.query(SysUser).filter(SysUser.id == id).first()
        if queue is None:
            return ReturnTool.ErrorReturn("用户未注册！")
        sql_data = {
            'id': id,
            'avatar': avatar,
            'nick_name': nick_name,
            "update_date": TimeToolClass.get_time()
        }
        # 使用 saveOrUpdate 函数
        result = DbTools.saveOrUpdate(session, sql_data, SysUser)
        if result:
            return ReturnTool.SuccessReturn()
        else:
            return ReturnTool.ErrorReturn('修改失败！')


def get_refresh_token(refresh_id):
    with DatabaseSession() as session:
        logs = session.query(SysUsersLoginLogs).filter(SysUsersLoginLogs.refresh_id == refresh_id).first()
        if logs is None:
            return ReturnTool.ErrorReturn("权限已失效", 401)
        token = logs.refresh_token
        jwt = JWTHandler()
        resp = jwt.decode_jwt(token)
        logs.update_date = datetime.datetime.now()
        session.commit()
        if resp['code'] == 200:
            payload = resp['data']
            login_token = jwt.encode_jwt(payload)
            return ReturnTool.SuccessReturn(login_token)
        else:
            return ReturnTool.ErrorReturn(resp['message'], resp['code'])


def query_login_user(req_user):
    with DatabaseSession() as session:
        half_moth = datetime.date.today() - relativedelta(days=15)
        logs = session.query(SysUsersLoginLogs).filter(and_(
            SysUsersLoginLogs.user_id == req_user.get('id'),
            SysUsersLoginLogs.create_date > half_moth
        )).all()
        res_arr = []
        jwt = JWTHandler()
        for log in logs:
            token = log.refresh_token
            resp = jwt.decode_jwt(token)
            if resp['code'] == 200:
                res_arr.append({
                    'id': log.id,
                    'name': log.name,
                    'refresh_id': log.refresh_id,
                    'ip': log.ip,
                    'update_date': log.update_date.strftime('%Y-%m-%d %H:%M:%S'),
                })

        return ReturnTool.SuccessReturn(res_arr)


def sing_out_device(request):
    data = request.get_json()
    if not data:
        return ReturnTool.ErrorReturn('参数为空！', 400)

    e_id = data.get('id')
    with DatabaseSession() as session:
        session.query(SysUsersLoginLogs).filter(SysUsersLoginLogs.id == e_id).delete()
        session.commit()
        return ReturnTool.SuccessReturn("退出成功！")


def update_sing_device(request):
    data = request.get_json()
    if not data:
        return ReturnTool.ErrorReturn('参数为空！', 400)

    e_id = data.get('id')
    e_name = data.get('name')
    with DatabaseSession() as session:
        logs = {
            'id': e_id,
            'name': e_name
        }
        DbTools.saveOrUpdate(session, logs, SysUsersLoginLogs)
        return ReturnTool.SuccessReturn("修改成功！")
