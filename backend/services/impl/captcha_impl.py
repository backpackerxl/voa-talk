import json

from utils import Captcha, ReturnTool
from utils.GetChatId import Snowflake

snowflake = Snowflake(data_center_id=1, worker_id=9)
from utils.RedisUtils import RedisHandler


def verify(token, user_x, trace):
    res = RedisHandler().get_key(token)
    if res is None:
        return ReturnTool.ErrorReturn("验证已过期")
    data = json.loads(res)

    features = Captcha.analyze_trace(trace)
    human_like = Captcha.is_human_like(features)
    if human_like is False:
        return ReturnTool.ErrorReturn("轨道图灵测试未通过")

    data["attempts"] += 1
    gap_x = data["gap_x"]

    if abs(user_x - gap_x) <= Captcha.ALLOWED_OFFSET:
        RedisHandler().save_key(token, json.dumps(True), 300)  # 通过后五分钟有效
        return ReturnTool.SuccessReturn({
            'refresh': True,
            'msg': "验证成功"
        })

    if data["attempts"] >= Captcha.MAX_ATTEMPTS:
        RedisHandler().remove_key(token)
        return ReturnTool.SuccessReturn({
            'refresh': False,
            'msg': "尝试次数过多，正在为你重新生成验证"
        })
    # 更新状态
    RedisHandler().save_key(token, json.dumps(data), RedisHandler().get_expire(token))
    return ReturnTool.ErrorReturn(f"验证失败，还剩 {Captcha.MAX_ATTEMPTS - data['attempts']} 次机会")


def refresh():
    data = Captcha.generate_captcha_image()
    token = str(snowflake.next_id())
    rd = {
        "gap_x": data["gap_x"],
        "attempts": 0
    }

    RedisHandler().save_key(token, json.dumps(rd), 300)  # 验证码5分钟内有效
    return ReturnTool.SuccessReturn({
        "bg_base64": data["bg_base64"],
        "slider_base64": data["slider_base64"],
        "token": token,
        "gap_y": data["gap_y"],
        "slider_width": data["slider_width"],
        "slider_height": data["slider_height"],
    })
