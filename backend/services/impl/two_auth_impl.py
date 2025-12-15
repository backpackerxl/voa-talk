import base64
import io
import json
import os
import secrets
import uuid
from datetime import datetime
from utils.Config import ALLOWED_ORIGINS

import pyotp
import qrcode
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
    PublicKeyCredentialDescriptor,
    AuthenticatorAttachment,
    ResidentKeyRequirement,
    AttestationConveyancePreference,
)

from dbinfo import DatabaseSession
from entity import SysUser
from utils import ReturnTool, DbTools
from utils import logs, TimeToolClass
from utils.RedisUtils import RedisHandler


def show_qr(username):
    # 检查用户是否存在
    with DatabaseSession() as session:
        queue = session.query(SysUser.otp_secrets).filter(SysUser.user_name == username).first()
        if not queue:
            return ReturnTool.ErrorReturn('用户不存在！', 404)

        # 获取用户的OTP密钥
        otp_secret = queue.otp_secrets

        # 创建TOTP对象
        totp = pyotp.totp.TOTP(otp_secret)

        # 生成用于Google Authenticator等应用的URI
        provisioning_uri = totp.provisioning_uri(
            name=username,
            issuer_name="2FA Voatalk App"
        )

        # 生成QR码
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)

        # 创建图像
        img = qr.make_image(fill_color="black", back_color="white")

        # 将图像转换为base64编码
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return ReturnTool.SuccessReturn({
            'username': username,
            'qr_code': f"data:image/png;base64,{img_str}"
        })


# 生成安全的挑战值
def generate_challenge():
    return secrets.token_bytes(32)


def register_begin(request):
    data = request.get_json()
    if not data:
        return ReturnTool.ErrorReturn('参数必填！', 400)

    username = data.get('username')
    if not username:
        return ReturnTool.ErrorReturn('用户名必填！', 400)

    with DatabaseSession() as session:
        queue = session.query(SysUser.credentials_data).filter(SysUser.user_name == username).first()
        # 检查用户是否已存在
        if queue.credentials_data:
            return ReturnTool.ErrorReturn('不能重复注册二次身份验证！', 409)

        # 生成挑战值
        challenge = generate_challenge()

        # 获取请求的主机名作为RP ID
        rp_id = request.host.split(':')[0]  # 去掉端口号

        # 生成注册选项
        options = generate_registration_options(
            rp_id=rp_id,
            rp_name=os.environ.get('RP_NAME', 'Voatalk'),
            user_id=username.encode('utf-8'),
            user_name=username,
            user_display_name=username,
            authenticator_selection=AuthenticatorSelectionCriteria(
                authenticator_attachment=AuthenticatorAttachment.CROSS_PLATFORM,
                resident_key=ResidentKeyRequirement.PREFERRED,
                user_verification=UserVerificationRequirement.PREFERRED,
                require_resident_key=False,
            ),
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

    # 保存凭证信息
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
        queue = session.query(SysUser.id).filter(SysUser.user_name == username).first()
        if not queue:
            return ReturnTool.ErrorReturn('用户不存在', 404)
        credentials_data = {
            'credential_id': bytes_to_base64url(verification.credential_id),
            'public_key': bytes_to_base64url(verification.credential_public_key),
            'sign_count': verification.sign_count,
            'transports': transport_enums,
            'registered_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'authenticator_name': 'Security Key',  # 可以从验证器获取
        }

        # 为用户生成OTP密钥
        otp_secret = pyotp.random_base32()

        sql_data = {
            'id': queue.id,
            'otp_secrets': otp_secret,
            'credentials_data': json.dumps(credentials_data),
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
                'username': username
            })
        else:
            return ReturnTool.ErrorReturn({
                'status': 'error',
                'message': '绑定失败！请联系管理员。',
                'username': username
            }, 500)


def generate_otp_qrcode(username):
    with DatabaseSession() as session:
        queue = session.query(SysUser.otp_secrets).filter(SysUser.user_name == username).first()
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
    if not username:
        return ReturnTool.ErrorReturn('用户名必填!', 400)

    # 检查用户是否存在
    with DatabaseSession() as session:
        queue = session.query(SysUser.credentials_data).filter(SysUser.user_name == username).first()
        if not queue.credentials_data:
            return ReturnTool.ErrorReturn('用户没有开通二次身份验证！', 404)

        credential = json.loads(queue.credentials_data)

        # 生成挑战值
        challenge = generate_challenge()

        # 生成认证选项
        # 安全地处理传输类型
        stored_transports = credential.get('transports', ['internal'])
        logs.setup_logger().info(f"Stored transports: {stored_transports}")
        logs.setup_logger().info(f"Stored transports type: {type(stored_transports)}")

        # 确保传输类型是AuthenticatorTransport枚举值而不是字符串
        from webauthn.helpers.structs import AuthenticatorTransport
        transport_enums = []

        if stored_transports:
            for i, t in enumerate(stored_transports):
                logs.setup_logger().info(f"Processing transport[{i}]: {t}, type: {type(t)}")
                try:
                    if isinstance(t, AuthenticatorTransport):  # 如果已经是枚举值
                        logs.setup_logger().info(f"Transport {t} is already an enum")
                        transport_enums.append(t)
                    elif isinstance(t, str):  # 如果是字符串
                        logs.setup_logger().info(f"Transport {t} is a string, converting to enum")
                        try:
                            transport_enums.append(AuthenticatorTransport(t))
                        except ValueError:
                            # 如果字符串不是有效的枚举值，使用默认值
                            logs.setup_logger().info(f"Transport {t} is not a valid enum, using default")
                            transport_enums.append(AuthenticatorTransport.INTERNAL)
                    else:  # 其他情况使用默认值
                        logs.setup_logger().info(f"Transport {t} is neither enum nor string, using default")
                        transport_enums.append(AuthenticatorTransport.INTERNAL)
                except Exception as e:
                    logs.setup_logger().error(f"Error processing transport[{i}] {t}: {str(e)}")
                    # 出错时使用默认值
                    transport_enums.append(AuthenticatorTransport.INTERNAL)
        else:
            transport_enums = [AuthenticatorTransport.INTERNAL]

        logs.setup_logger().info(f"Final transport enums: {transport_enums}")

        # 创建凭证描述符
        from webauthn.helpers.structs import PublicKeyCredentialType
        credential_descriptor = PublicKeyCredentialDescriptor(
            id=base64url_to_bytes(credential['credential_id']),
            type=PublicKeyCredentialType.PUBLIC_KEY,
            transports=transport_enums,
        )
        logs.setup_logger().info(f"Credential descriptor created: {credential_descriptor}")

        # 获取请求的主机名作为RP ID
        rp_id = request.host.split(':')[0]  # 去掉端口号

        # 生成认证选项
        logs.setup_logger().info("Calling generate_authentication_options")
        options = generate_authentication_options(
            rp_id=rp_id,
            allow_credentials=[credential_descriptor],
            user_verification=UserVerificationRequirement.PREFERRED,
            challenge=challenge,
            timeout=60000,
        )
        logs.setup_logger().info("generate_authentication_options completed successfully")

        # 保存挑战值和用户信息到 redis
        req_id = str(uuid.uuid4())
        auth_user = {
            'authentication_challenge': bytes_to_base64url(challenge),
            'authentication_username': username
        }
        RedisHandler().save_key(req_id, json.dumps(auth_user), 300)  # 链接5分钟保活

        # 转换选项为 JSON
        options_json = options_to_json(options)
        options_dict = json.loads(options_json)
        options_dict['challenge'] = bytes_to_base64url(challenge)
        options_dict['req_id'] = req_id

        return ReturnTool.SuccessReturn(options_dict)


def login_complete(request):
    data = request.get_json()
    if not data:
        return ReturnTool.ErrorReturn('参数为空！', 400)

    # 从 redis 获取挑战值和用户名
    req_id = data.get('req_id')
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
        queue = session.query(SysUser.id, SysUser.credentials_data).filter(SysUser.user_name == username).first()
        if not queue.credentials_data:
            return ReturnTool.ErrorReturn('用户没有开通二次身份验证！', 404)

        stored_credential = json.loads(queue.credentials_data)

        # 转换挑战值为字节
        expected_challenge = base64url_to_bytes(challenge_base64)

        # 解析凭证数据
        credential = parse_authentication_credential_json(data)

        # 获取请求的主机名作为RP ID
        rp_id = request.host.split(':')[0]  # 去掉端口号

        # 验证认证响应
        verification = verify_authentication_response(
            credential=credential,
            expected_challenge=expected_challenge,
            expected_origin=request.host_url.rstrip('/'),
            expected_rp_id=rp_id,
            credential_public_key=base64url_to_bytes(stored_credential['public_key']),
            credential_current_sign_count=stored_credential['sign_count'],
            require_user_verification=False,
        )

        # 更新签名计数
        stored_credential['sign_count'] = verification.new_sign_count

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

        return ReturnTool.SuccessReturn({
            'status': 'ok',
            'message': '验证通过！',
            'username': username,
            'authenticated': True
        })


def verify_otp(request):
    data = request.get_json()
    if not data:
        return ReturnTool.ErrorReturn('参数为空！', 400)

    username = data.get('username')
    otp_code = data.get('otp_code')

    if not username or not otp_code:
        return ReturnTool.ErrorReturn('二次验证码和用户名必填！', 400)

    # 检查用户是否存在
    with DatabaseSession() as session:
        queue = session.query(SysUser.otp_secrets).filter(SysUser.user_name == username).first()
        if not queue.otp_secrets:
            return ReturnTool.ErrorReturn('用户没有开通OTP二次身份验证！', 404)
        # 获取用户的OTP密钥
        otp_secret = queue.otp_secrets

        # 创建TOTP对象并验证OTP代码
        totp = pyotp.TOTP(otp_secret)
        if totp.verify(otp_code):
            userinfo = RedisHandler().get_key("user:info:" + username)
            user_login_info = None
            if userinfo:
                user_login_info = json.loads(userinfo)

            return ReturnTool.SuccessReturn({
                'status': 'ok',
                'message': '验证成功!',
                'username': username,
                'userinfo': user_login_info
            })
        else:
            return ReturnTool.SuccessReturn({
                'status': 'error',
                'message': '验证码错误!',
                'username': username
            })
