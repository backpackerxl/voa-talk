import base64
import datetime
import hashlib

from Crypto.Cipher import AES

from dbinfo import DatabaseSession
from entity import SysUser
from utils import ReturnTool
from utils.BusinessException import ResultCode, BusinessException
from utils.JwtUtils import JWTHandler
from utils.encryptUtils import aes_decrypt


# 加密（编码）函数
def encrypt(plaintext):
    """
    加密（编码）函数
    :param plaintext:
    :return:
    """
    encoded_bytes = base64.b64encode(plaintext.encode("utf-8"))
    encoded_str = encoded_bytes.decode("utf-8")
    return encoded_str


def decrypt_aes(ciphertext):
    """
    对称解密
    :param ciphertext:
    :return:
    """
    try:
        key = b"hnciquewhngfo1qc"
        cipher = AES.new(key, AES.MODE_CBC, iv=b'\x00' * 16)
        plaintext_bytes = cipher.decrypt(base64.b64decode(ciphertext))
        plaintext = plaintext_bytes.decode('utf-8').rstrip('\x00').rstrip('\x10')
    except:
        # 密码解密失败
        error_code, message = ResultCode.get_code('PASSWORD_DECRYPTION_FAILED'), ResultCode.get_msg(
            'PASSWORD_DECRYPTION_FAILED')
        raise BusinessException(error_code, message)
    return plaintext


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


def login_impl(request):
    with DatabaseSession() as session:
        ip = request.remote_addr
        queue = session.query(SysUser).filter(SysUser.user_name == request.get_json().get("userName")).first()

        # 如果用户不存在
        if not queue:
            return ReturnTool.ErrorReturn("用户不存在")
        if queue.user_state != 1:
            return ReturnTool.ErrorReturn("用户已经停用，请联系管理员！")
        pwd = request.get_json().get('passWord')
        decrypt = aes_decrypt(pwd)
        password = verify_password(decrypt, queue.salt)

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
            "IP": ip,
            "superAdmin": queue.super_admin
        }
        # 生成token
        token = JWTHandler().encode_jwt(user_data)
        user_data["jwtToken"] = token
        user_data["refreshToken"] = token
        returnData = ReturnTool.SuccessReturn(user_data)
        return returnData
