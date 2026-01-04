import base64
import io
import json
import os
import secrets
import uuid
from datetime import datetime

import pyotp
import qrcode
from sqlalchemy import or_
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    generate_authentication_options,
    verify_authentication_response,
    options_to_json,
)
from webauthn.helpers import (
    parse_authentication_credential_json,
    parse_registration_credential_json,
    base64url_to_bytes,
    bytes_to_base64url,
)
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    UserVerificationRequirement,
    AuthenticatorAttachment,
    ResidentKeyRequirement,
    AttestationConveyancePreference,
)

from dbinfo import DatabaseSession
from entity import SysUser
from utils import ReturnTool, DbTools
from utils import logs, TimeToolClass
from utils.Config import ALLOWED_ORIGINS
from utils.JwtUtils import JWTHandler
from utils.RedisUtils import RedisHandler
from utils.Tools import generate_random_recovery_code, generate_hashed_password, verify_password
from utils.encryptUtils import encrypt_aes, aes_decrypt


# 生成安全的挑战值
def generate_challenge():
    return secrets.token_bytes(32)


def register_begin(request):
    data = request.get_json()
    if not data:
        return ReturnTool.ErrorReturn('参数必填！', 400)

    username = data.get('username')
    platform = data.get('platform')
    supported = data.get('supported')
    if not username:
        return ReturnTool.ErrorReturn('用户名必填！', 400)

    with DatabaseSession() as session:
        queue = session.query(SysUser.credentials_data, SysUser.credentials_data_mobile).filter(or_(
            SysUser.user_name == username,
            SysUser.email == username,
        )).first()
        # 检查用户凭证是否已存在
        if platform == 'mobile':
            if queue.credentials_data_mobile:
                return ReturnTool.ErrorReturn('不能重复注册二次身份验证！', 409)
        else:
            if queue.credentials_data:
                return ReturnTool.ErrorReturn('不能重复注册二次身份验证！', 409)

        # 生成挑战值
        challenge = generate_challenge()

        # 获取请求的主机名作为RP ID
        rp_id = request.host.split(':')[0]  # 去掉端口号
        if supported:
            authenticator_selection = AuthenticatorSelectionCriteria(
                authenticator_attachment=AuthenticatorAttachment.PLATFORM,
                resident_key=ResidentKeyRequirement.REQUIRED,
                user_verification=UserVerificationRequirement.REQUIRED,
                require_resident_key=False,
            )
        else:
            authenticator_selection = AuthenticatorSelectionCriteria(
                authenticator_attachment=AuthenticatorAttachment.CROSS_PLATFORM,
                resident_key=ResidentKeyRequirement.PREFERRED,
                user_verification=UserVerificationRequirement.PREFERRED,
                require_resident_key=False,
            )

        # 生成注册选项
        options = generate_registration_options(
            rp_id=rp_id,
            rp_name=os.environ.get('RP_NAME', 'Voatalk'),
            user_id=username.encode('utf-8'),
            user_name=username,
            user_display_name=username,
            authenticator_selection=authenticator_selection,
            challenge=challenge,
            timeout=60000,  # 60秒超时
            attestation=AttestationConveyancePreference.NONE,  # 生产环境可能需要 "direct"
            exclude_credentials=[],  # 排除已存在的凭证
        )

        # 保存挑战值和用户信息到 redis
        req_id = str(uuid.uuid4())
        reg_user = {
            'registration_challenge': bytes_to_base64url(challenge),
            'registration_username': username
        }
        RedisHandler().save_key(req_id, json.dumps(reg_user), 300)  # 链接5分钟保活

        # 转换选项为 JSON
        options_json = options_to_json(options)

        # 确保 challenge 是字符串
        options_dict = json.loads(options_json)
        options_dict['challenge'] = bytes_to_base64url(challenge)
        options_dict['req_id'] = req_id

        return ReturnTool.SuccessReturn(options_dict)


def register_complete(request):
    data = request.get_json()
    if not data:
        return ReturnTool.ErrorReturn('参数必填！', 400)

    req_id = data.get('req_id')
    platform = data.get('platform')
    cha_res_str = RedisHandler().get_key(req_id)
    if not cha_res_str:
        return ReturnTool.ErrorReturn('挑战注册已过期或错误！', 400)
    cha_res = json.loads(cha_res_str)
    logs.setup_logger().info(f"Session data: {cha_res}")

    # 从 session 获取挑战值和用户名
    challenge_base64 = cha_res.get('registration_challenge')
    username = cha_res.get('registration_username')

    logs.setup_logger().info(f"Challenge from session: {challenge_base64}")
    logs.setup_logger().info(f"Username from session: {username}")

    if not challenge_base64 or not username:
        return ReturnTool.ErrorReturn('挑战注册已过期或错误！', 400)

    # 转换挑战值为字节
    expected_challenge = base64url_to_bytes(challenge_base64)

    # 解析凭证数据
    credential = parse_registration_credential_json(data)

    # 获取请求的主机名作为RP ID
    rp_id = request.host.split(':')[0]  # 去掉端口号
    # 核心：从请求头获取真实的客户端 Origin，校验是否在白名单内
    client_origin = request.headers.get("Origin")
    if client_origin not in ALLOWED_ORIGINS:
        raise ValueError(f"Unexpected client data origin \"{client_origin}\", expected one of {ALLOWED_ORIGINS}")

    # 验证注册响应
    verification = verify_registration_response(
        credential=credential,
        expected_challenge=expected_challenge,
        expected_origin=client_origin,
        expected_rp_id=rp_id,
        require_user_verification=False,
    )

    # 保存凭证信息 transport: ["usb", "nfc", "ble", "internal"] // 支持CTAP的传输类型
    transports = credential.response.transports if hasattr(credential.response,
                                                           'transports') and credential.response.transports else [
        'internal']
    # 将字符串转换为AuthenticatorTransport枚举值
    from webauthn.helpers.structs import AuthenticatorTransport
    transport_enums = []
    for transport in transports:
        try:
            transport_enums.append(AuthenticatorTransport(transport))
        except ValueError:
            # 如果传输类型不匹配，使用默认值
            transport_enums.append(AuthenticatorTransport.INTERNAL)

    with DatabaseSession() as session:
        queue = session.query(SysUser.id).filter(or_(
            SysUser.user_name == username,
            SysUser.email == username,
        )).first()
        if not queue:
            return ReturnTool.ErrorReturn('用户不存在', 404)
        credentials_data = {
            'credential_id': bytes_to_base64url(verification.credential_id),
            'public_key': bytes_to_base64url(verification.credential_public_key),
            'sign_count': verification.sign_count,
            'transports': transport_enums,
            'registered_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'authenticator_name': 'Security App',  # 可以从验证器获取
        }

        recovery_code = generate_random_recovery_code()
        recovery_code_md5 = [generate_hashed_password(code) for code in recovery_code]

        # 为用户生成OTP密钥
        otp_secret = pyotp.random_base32()

        if platform == 'mobile':
            sql_data = {
                'id': queue.id,
                'credentials_data_mobile': json.dumps(credentials_data),
                "update_date": TimeToolClass.get_time()
            }
        else:
            sql_data = {
                'id': queue.id,
                'otp_secrets': otp_secret,
                'credentials_data': json.dumps(credentials_data),
                'recovery_code_md5': json.dumps(recovery_code_md5),
                "update_date": TimeToolClass.get_time()
            }

        # 使用 saveOrUpdate 函数
        result = DbTools.saveOrUpdate(session, sql_data, SysUser)
        if result:
            # 清理 redis
            RedisHandler().remove_key(req_id)
            logs.setup_logger().info(f"User {username} registered successfully")
            return ReturnTool.SuccessReturn({
                'status': 'ok',
                'message': '绑定成功！',
                'fa_recovery_code': [encrypt_aes(code) for code in recovery_code],
                'username': username
            })
        else:
            return ReturnTool.ErrorReturn('绑定失败！请联系管理员。', 500)


def generate_otp_qrcode(username):
    with DatabaseSession() as session:
        queue = session.query(SysUser.otp_secrets).filter(
            or_(
                SysUser.user_name == username,
                SysUser.email == username,
            )).first()
        if not queue:
            return ReturnTool.ErrorReturn('用户不存在!', 404)

        # 获取用户的OTP密钥
        otp_secret = queue.otp_secrets

        # 创建TOTP对象
        totp = pyotp.totp.TOTP(otp_secret)

        # 生成用于Google Authenticator等应用的URI
        provisioning_uri = totp.provisioning_uri(
            name=username,
            issuer_name="VoaTalk",
            image="https://voatalk.online/voatalk_api/uploads/20251215/logo.png"
        )

        # 生成QR码
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)

        # 创建图像
        img = qr.make_image(fill_color="black", back_color="white")

        # 将图像转换为base64编码
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return ReturnTool.SuccessReturn({
            'status': 'ok',
            'qrcode': img_str,
            'secret': otp_secret,
            'provisioning_uri': provisioning_uri
        })


def login_begin(request):
    data = request.get_json()
    if not data:
        return ReturnTool.ErrorReturn('参数为空！', 400)

    username = data.get('username')
    platform = data.get('platform')
    supported = data.get('supported')
    if not username:
        return ReturnTool.ErrorReturn('用户名必填!', 400)

    # 检查用户是否存在（新增：判空 queue，避免 AttributeError）
    with DatabaseSession() as session:
        queue = session.query(SysUser.user_name, SysUser.credentials_data, SysUser.credentials_data_mobile).filter(or_(
            SysUser.user_name == username,
            SysUser.email == username,
        )).first()
        if not queue or not queue.user_name:
            return ReturnTool.ErrorReturn('用户未注册！', 400)
        if platform == 'mobile':
            if not queue or not queue.credentials_data_mobile:  # 新增 queue 判空
                return ReturnTool.ErrorReturn('用户没有开通移动端二次身份验证！', 404)
            credential = json.loads(queue.credentials_data_mobile)
        else:
            if not queue or not queue.credentials_data:  # 新增 queue 判空
                return ReturnTool.ErrorReturn('用户没有开通PC端二次身份验证！', 404)
            credential = json.loads(queue.credentials_data)

        # 生成挑战值（确保是32字节随机数，符合WebAuthn规范）
        challenge = generate_challenge()  # 需确保该函数返回 bytes 类型，长度建议32

        # 处理传输类型（逻辑不变，保留日志）
        stored_transports = credential.get('transports', ['internal'])
        logs.setup_logger().info(f"Stored transports: {stored_transports}")

        from webauthn.helpers.structs import AuthenticatorTransport
        transport_enums = []
        if stored_transports:
            for i, t in enumerate(stored_transports):
                try:
                    if isinstance(t, AuthenticatorTransport):
                        transport_enums.append(t)
                    elif isinstance(t, str):
                        transport_enums.append(AuthenticatorTransport(t.lower()))  # 新增：统一小写，避免枚举匹配失败
                    else:
                        transport_enums.append(AuthenticatorTransport.INTERNAL)
                except Exception as e:
                    logs.setup_logger().error(f"Transport error: {e}")
                    transport_enums.append(AuthenticatorTransport.INTERNAL)
        else:
            transport_enums = [AuthenticatorTransport.INTERNAL]

        # 创建凭证描述符（确保 credential_id 解码正确）
        from webauthn.helpers.structs import PublicKeyCredentialDescriptor, PublicKeyCredentialType
        try:
            cred_id_bytes = base64url_to_bytes(credential['credential_id'])  # 关键：确保该函数能正确解码前端存储的 credential_id
        except Exception as e:
            logs.setup_logger().error(f"Credential ID decode error: {e}")
            return ReturnTool.ErrorReturn('凭证ID格式错误', 400)

        credential_descriptor = PublicKeyCredentialDescriptor(
            id=cred_id_bytes,
            type=PublicKeyCredentialType.PUBLIC_KEY,
            transports=transport_enums,
        )

        # 生成验证场景选项（删除多余的 pubKeyCredParams，验证场景不需要）
        rp_id = request.host.split(':')[0]
        if supported:
            user_verification = UserVerificationRequirement.REQUIRED
        else:
            user_verification = UserVerificationRequirement.PREFERRED

        options = generate_authentication_options(
            rp_id=rp_id,
            allow_credentials=[credential_descriptor],
            user_verification=user_verification,
            challenge=challenge,  # 直接传 bytes 类型的 challenge
            timeout=60000,
        )

        # 保存挑战值到Redis（确保编码规范）
        req_id = str(uuid.uuid4())
        auth_user = {
            'authentication_challenge': bytes_to_base64url(challenge),  # 确保该函数返回 无填充符 的 Base64URL
            'authentication_username': username
        }
        RedisHandler().save_key(req_id, json.dumps(auth_user), 300)

        # 转换选项为JSON（关键：使用官方工具，避免手动修改导致格式错误）
        options_json = options_to_json(options)
        options_dict = json.loads(options_json)
        # 仅补充必要字段，删除 pubKeyCredParams（验证场景不需要）
        options_dict['req_id'] = req_id
        # 确保 challenge 是 纯Base64URL格式（无填充符、符号替换正确）
        options_dict['challenge'] = bytes_to_base64url(challenge)

        # 最终返回：确保返回的是JSON格式，且所有Base64URL字段无非法字符
        return ReturnTool.SuccessReturn(options_dict)


def login_complete(request):
    data = request.get_json()
    if not data:
        return ReturnTool.ErrorReturn('参数为空！', 400)

    # 从 redis 获取挑战值和用户名
    req_id = data.get('req_id')
    platform = data.get('platform')
    auth_cha_str = RedisHandler().get_key(req_id)
    if not auth_cha_str:
        return ReturnTool.ErrorReturn('请先生成挑战验证信息！', 400)
    auth_cha = json.loads(auth_cha_str)
    challenge_base64 = auth_cha.get('authentication_challenge')
    username = auth_cha.get('authentication_username')

    if not challenge_base64 or not username:
        return ReturnTool.ErrorReturn('挑战验证信息已过期或错误！', 400)

    # 检查用户是否存在
    with DatabaseSession() as session:
        queue = session.query(SysUser).filter(or_(
            SysUser.user_name == username,
            SysUser.email == username,
        )).first()
        if queue.user_state != 1:
            return ReturnTool.ErrorReturn("用户已经停用，请联系管理员！")
        if platform == 'mobile':
            if not queue or not queue.credentials_data_mobile:  # 新增 queue 判空
                return ReturnTool.ErrorReturn('用户没有开通移动端二次身份验证！', 404)
            stored_credential = json.loads(queue.credentials_data_mobile)
        else:
            if not queue or not queue.credentials_data:  # 新增 queue 判空
                return ReturnTool.ErrorReturn('用户没有开通PC端二次身份验证！', 404)
            stored_credential = json.loads(queue.credentials_data)

        # 转换挑战值为字节
        expected_challenge = base64url_to_bytes(challenge_base64)

        # 解析凭证数据
        credential = parse_authentication_credential_json(data)

        # 获取请求的主机名作为RP ID
        rp_id = request.host.split(':')[0]  # 去掉端口号

        # 核心：从请求头获取真实的客户端 Origin，校验是否在白名单内
        client_origin = request.headers.get("Origin")
        if client_origin not in ALLOWED_ORIGINS:
            raise ValueError(f"Unexpected client data origin \"{client_origin}\", expected one of {ALLOWED_ORIGINS}")

        # 验证认证响应
        verification = verify_authentication_response(
            credential=credential,
            expected_challenge=expected_challenge,
            expected_origin=client_origin,
            expected_rp_id=rp_id,
            credential_public_key=base64url_to_bytes(stored_credential['public_key']),
            credential_current_sign_count=stored_credential['sign_count'],
            require_user_verification=False,
        )

        # 更新签名计数
        stored_credential['sign_count'] = verification.new_sign_count

        if platform == 'mobile':
            sql_data = {
                'id': queue.id,
                'credentials_data_mobile': json.dumps(stored_credential),
                "update_date": TimeToolClass.get_time()
            }
        else:
            sql_data = {
                'id': queue.id,
                'credentials_data': json.dumps(stored_credential),
                "update_date": TimeToolClass.get_time()
            }

        # 使用 saveOrUpdate 函数
        DbTools.saveOrUpdate(session, sql_data, SysUser)
        # 清理 redis
        RedisHandler().remove_key(req_id)

        logs.setup_logger().info(f"User {username} logged in successfully")

        # 准备返回数据
        user_data = {
            "id": queue.id,
            "userName": queue.user_name,
            "nickName": queue.nick_name,
            "avatar": queue.avatar,
            "email": queue.email,
            "loginType": "voatalk",
            "IP": request.remote_addr,
            "superAdmin": queue.super_admin,
            "bindQQ": (1 if queue.qq_open_id is None else 3),
            "bindGithub": (1 if queue.github_open_id is None else 3),
        }
        # 生成token
        token = JWTHandler().encode_jwt(user_data)
        user_data["jwtToken"] = token
        user_data["refreshToken"] = token
        user_data['exp'] = user_data['exp'].strftime("%Y-%m-%d %H:%M:%S")

        return ReturnTool.SuccessReturn({
            'status': 'ok',
            'message': '验证通过！',
            'username': username,
            'authenticated': True,
            'userinfo': user_data
        })


def verify_otp(request):
    data = request.get_json()
    if not data:
        return ReturnTool.ErrorReturn('参数为空！', 400)

    username = data.get('username')
    otp_code = data.get('otp_code')
    next_id = data.get('next_id')

    if not username or not otp_code:
        return ReturnTool.ErrorReturn('二次验证码和用户名必填！', 400)

    # 检查用户是否存在
    with DatabaseSession() as session:
        queue = session.query(SysUser.otp_secrets).filter(or_(
            SysUser.user_name == username,
            SysUser.email == username,
        )).first()
        if not queue.otp_secrets:
            return ReturnTool.ErrorReturn('用户没有开通OTP二次身份验证！', 404)
        # 获取用户的OTP密钥
        otp_secret = queue.otp_secrets

        # 创建TOTP对象并验证OTP代码
        totp = pyotp.TOTP(otp_secret)
        if totp.verify(otp_code):
            userinfo = RedisHandler().get_key("user:info:" + next_id)
            if userinfo:
                user_login_info = json.loads(userinfo)
                RedisHandler().remove_key("user:info:" + next_id)
                return ReturnTool.SuccessReturn({
                    'status': 'ok',
                    'message': '验证成功!',
                    'username': username,
                    'userinfo': user_login_info
                })
            else:
                return ReturnTool.ErrorReturn('登录信息已过期，请重新登录！', 301)
        else:
            return ReturnTool.ErrorReturn('验证码错误!', 401)


def verify_recovery(request):
    data = request.get_json()
    if not data:
        return ReturnTool.ErrorReturn('参数为空！', 400)

    username = data.get('username')
    recovery_code = aes_decrypt(data.get('recovery_code'))
    next_id = data.get('next_id')

    if not username or not recovery_code:
        return ReturnTool.ErrorReturn('恢复码和用户名必填！', 400)

    # 检查用户是否存在
    with DatabaseSession() as session:
        queue = session.query(SysUser.recovery_code_md5, SysUser.id).filter(or_(
            SysUser.user_name == username,
            SysUser.email == username,
        )).first()
        if not queue.recovery_code_md5:
            return ReturnTool.ErrorReturn('用户没有开通恢复码！', 404)
        # 获取用户的OTP密钥
        recovery_code_arr = json.loads(queue.recovery_code_md5)
        if len(recovery_code_arr) == 0:
            return ReturnTool.ErrorReturn('恢复码已用完，请联系管理员!', 404)
        recovery_code_arr_new = [sub_arr for sub_arr in recovery_code_arr if
                                 sub_arr[0] != verify_password(recovery_code, sub_arr[1])]
        if len(recovery_code_arr) == len(recovery_code_arr_new):
            return ReturnTool.ErrorReturn('恢复码错误!', 401)
        else:
            userinfo = RedisHandler().get_key("user:info:" + next_id)
            if userinfo:
                user_login_info = json.loads(userinfo)
                sql_data = {
                    'id': queue.id,
                    'recovery_code_md5': json.dumps(recovery_code_arr_new),
                    "update_date": TimeToolClass.get_time()
                }
                DbTools.saveOrUpdate(session, sql_data, SysUser)
                RedisHandler().remove_key("user:info:" + next_id)
                return ReturnTool.SuccessReturn({
                    'status': 'ok',
                    'message': f'验证成功, 还剩{len(recovery_code_arr_new)}次机会！',
                    'username': username,
                    'userinfo': user_login_info
                })
            else:
                return ReturnTool.ErrorReturn('登录信息已过期，请重新登录！', 301)
