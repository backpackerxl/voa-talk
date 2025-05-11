import base64
import datetime
import hashlib
import os
import random
import string
import sys
from io import BytesIO

from Crypto.Cipher import AES
from PIL import Image, ImageDraw, ImageFont
from captcha.image import ImageCaptcha

from dbinfo import DatabaseSession
from entity import SysUser
from utils import SendMail, ReturnTool, Tools, encryptUtils, TimeToolClass, DbTools
from utils.BusinessException import ResultCode, BusinessException
from utils.JwtUtils import JWTHandler
from utils.RedisUtils import RedisHandler
from utils.encryptUtils import aes_decrypt


def generate_simple_captcha(size=4, width=100, height=40, font_size=24):
    # 生成随机字符串
    characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choices(characters, k=size))

    # 创建一个新的图像
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # PIL自带的字体
    try:
        font = ImageFont.load_default()
    except IOError:
        font = ImageFont.truetype("arial.ttf", font_size)

    # 在图像上写入验证码字符
    for i in range(size):
        draw.text((10 + i * font_size, 5), code[i], (0, 0, 0), font=font)

    # 保存图像到一个BytesIO对象
    image_data = BytesIO()
    image.save(image_data, format='JPEG')

    # 将图像数据转换为Base64编码的字符串
    base64_image = base64.b64encode(image_data.getvalue()).decode('utf-8')

    return code, base64_image


def generate_verification_code_scheme(size=4):
    characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choices(characters, k=size))

    # 确定字体文件的路径
    if getattr(sys, 'frozen', False):
        # 如果是exe文件，使用exe文件的目录
        base_path = os.path.dirname(sys.executable)
    else:
        # 如果不是exe文件，使用当前文件的目录
        base_path = os.path.dirname(__file__)

    # 字体文件的相对路径
    font_rel_path = os.path.join('fonts', 'ttf', 'ariblk.ttf')

    # 构建字体文件的绝对路径
    font_abs_path = os.path.join(base_path, font_rel_path)

    # 使用指定字体文件的ImageCaptcha生成验证码图像
    image = ImageCaptcha(fonts=[font_abs_path])

    # 生成图像数据
    data = image.generate(code)
    image_data = BytesIO(data.read())

    # 将图像数据转换为 Base64 编码的字符串
    base64_image = base64.b64encode(image_data.getvalue()).decode('utf-8')

    return code, base64_image


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


def getverifycode_impl():
    """

    :return:
    """
    # 生成验证码图片
    image, binary_data = generate_verification_code_scheme()
    image = encrypt(image.lower())  # 将验证码转换为小写再加密

    # 将验证码放入Redis，缓存时长
    RedisHandler().save_code(image, 60)
    # 将字节数据转换为base64编码的字符串
    returnData = {
        "status": "成功", "code": 200, "message": "操作成功",
        "data": {
            "key": image.lower(),
            "vCode": binary_data
        }
    }

    return returnData


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
    salted_input = input_password + salt  # 将用户输入的密码和盐值结合起来
    hashed_input = hashlib.sha256(salted_input.encode()).hexdigest()  # 对结合后的字符串进行 SHA-256 哈希处理

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
        # print(f"用户输入：{password}")
        # print(f"数据库存储：{queue.pass_word}")
        if password != queue.pass_word:
            return ReturnTool.ErrorReturn("密码错误")
        # 设置用户最后登录时间
        queue.last_login_time = datetime.datetime.now()
        session.commit()
        # 准备返回数据
        user_data = {
            "id": queue.id,
            "userName": queue.user_name,
            "nickName": queue.nick_name,
            "avatar": queue.avatar,
            "IP": ip,
            "superAdmin": queue.super_admin
        }
        # 生成token
        token = JWTHandler().encode_jwt(user_data)
        user_data["jwtToken"] = token
        user_data["refreshToken"] = token
        returnData = ReturnTool.SuccessReturn(user_data)
        return returnData


def get_the_email_verification_code_servie(email):
    """
    邮箱验证码
    :param email:
    :return:
    """
    with DatabaseSession() as session:
        queue = session.query(SysUser).filter(SysUser.email == email).first()
        if not queue:
            return ReturnTool.ErrorReturn("邮箱输入错误")
        # 生成验证码图片
        image, binary_data = generate_verification_code_scheme()
        image = image.lower()  # 将验证码转换为小写再加密
        image_email = f"{email}_{image}"
        # 将验证码放入Redis，缓存时长
        RedisHandler().save_code(image_email, 300)
        subject = "修改密码"
        body = f'您好：{queue.nick_name}\n您的账号正在找回密码。\n你的验证码为：{image}。'
        if SendMail.send_email(email, subject, body) != '电子邮件发送成功！':
            return ReturnTool.ErrorReturn('邮件发送失败，请检查邮箱是否正确')
        return ReturnTool.SuccessReturn("验证码已发送")


def retrieve_password_servie_servie(email, code):
    """
    验证账户与验证码
    """
    image_email = f"{email}_{code}"
    if RedisHandler().check_code(image_email) is False:
        return ReturnTool.ErrorReturn("验证码无效或已过期，请重新获取验证码")
    password = Tools.generate_random_password()
    hash_password = encryptUtils.encrypt_aes(password)
    hashed_password, salt = Tools.generate_hashed_password(hash_password)
    with DatabaseSession() as session:
        queue = session.query(SysUser).filter(SysUser.email == email).first()
        sql_data = {
            'id': queue.id, 'pass_word': hashed_password, 'salt': salt, "update_date": TimeToolClass.get_time()
        }
        subject = "欢迎使用VoaTalk"
        body = f'您好：{queue.name}\n您的账号密码找回成功。\n您的登录账号为：' + queue.user_name + '\n密码为：' + password + '\n请妥善保管您的账号密码。'
        if SendMail.send_email(email, subject, body) != '电子邮件发送成功！':
            return ReturnTool.ErrorReturn('邮件发送失败，请检查邮箱是否正确')
        DbTools.saveOrUpdate(session, sql_data, SysUser)
    return ReturnTool.SuccessReturn()
