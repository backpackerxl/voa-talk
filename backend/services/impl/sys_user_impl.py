import hashlib
import json
import uuid

from dbinfo import DatabaseSession
from sqlalchemy import or_
from dto import SysUserDTO
from entity import SysUser
from utils import DbTools, Config, encryptUtils, Tools
from utils import ReturnTool
import bcrypt

from utils import TimeToolClass

from utils import SendMail
from utils.GetChatId import Snowflake
from utils.RedisUtils import RedisHandler
from utils.encryptUtils import aes_decrypt

snowflake = Snowflake(data_center_id=1, worker_id=2)


def api_sys_user_find_list_page_impl(page_size, page_index, search_criteria):
    with DatabaseSession() as session:
        query = session.query(SysUserDTO)
        # 使用公用方法动态添加搜索条件
        query = DbTools.apply_filters(query, SysUser, search_criteria)
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


def enroll_impl(name, username, email):
    """
    用户注册服务
    :param name:
    :param username:
    :param email:
    :return:
    """
    password = Tools.generate_random_password()
    subject = "欢迎使用VoaTalk"
    body = f'您好：{name}\n您的账号已经注册成功。\n您的登录账号为：' + username + '\n密码为：' + password + '\n请妥善保管您的账号密码。'
    with DatabaseSession() as session:
        user_exist = session.query(SysUser).filter(
            or_(
                SysUser.user_name == username,
                SysUser.email == email,
            )
        ).all()
        if user_exist:
            return ReturnTool.ErrorReturn('用户名已存在或邮箱已被注册')
        if SendMail.send_email(email, subject, body) != '电子邮件发送成功！':
            return ReturnTool.ErrorReturn('邮件发送失败，请检查邮箱是否正确')
        hashed_password, salt = Tools.generate_hashed_password(password)
        sql_data = {
            'user_name': username, 'nick_name': name, 'email': email, 'pass_word': hashed_password, 'salt': salt,
            "update_date": TimeToolClass.get_time(), "create_date": TimeToolClass.get_time(),
            "super_admin": 0, "user_state": 1
        }
        DbTools.saveOrUpdate(session, sql_data, SysUser)
    return ReturnTool.SuccessReturn()


def forget_pwd_impl(email, req_url):
    subject = "欢迎使用VoaTalk"
    with DatabaseSession() as session:
        user_exist = session.query(SysUser).filter_by(email=email).first()
        if user_exist:
            # 存在此用户
            key = str(snowflake.next_id())
            body = f'您好：{user_exist.nick_name}\n您的登录账号为：' + user_exist.user_name + '，请点击此链接：\n' + req_url + '/' + key + '\n找回密码。注意：此链接10分钟内有效！'
            if SendMail.send_email(email, subject, body) != '电子邮件发送成功！':
                return ReturnTool.ErrorReturn('邮件发送失败，请检查邮箱是否正确')
            else:
                RedisHandler().save_key(key, json.dumps({
                    "user_name": user_exist.user_name,
                    "email": user_exist.email,
                }), 600)  # 链接10分钟保活
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


def api_user_update_nickname(id, avatar, nick_name):
    with DatabaseSession() as session:
        queue = session.query(SysUser).filter(SysUser.id == id).first()
        if queue is None:
            return ReturnTool.ErrorReturn("用户未注册！")
        sql_data = {
            'id': id,
            'avatar': avatar,
            'nick_name': nick_name
        }
        # 使用 saveOrUpdate 函数
        result = DbTools.saveOrUpdate(session, sql_data, SysUser)
        if result:
            return ReturnTool.SuccessReturn()
        else:
            return ReturnTool.ErrorReturn('修改失败！')
