import base64
import io
import json
import random

import requests
from PIL import Image, ImageDraw

# 配置参数
BG_W = 260
BG_H = 150
BACKGROUND_URL = f"https://picsum.photos/{BG_W}/{BG_H}"  # 使用固定尺寸图片
SLIDER_WIDTH = 40  # 滑块宽度
SLIDER_HEIGHT = 40  # 滑块高度
GAP_Y_RANGE = (0, 180)  # 缺口垂直位置范围
MAX_ATTEMPTS = 3  # 最大尝试次数
ALLOWED_OFFSET = 8  # 允许的像素误差


def generate_notch_mask(width, height):
    """生成带凹凸边缘的缺口遮罩"""
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)

    # 绘制基本矩形
    draw.rectangle((0, 0, width, height), fill=255)

    # 添加随机凹凸边缘
    for i in range(3):
        # 左侧凹凸
        y = random.randint(height // 4, height * 3 // 4)
        radius = random.randint(5, 10)
        draw.ellipse((-radius, y - radius, radius, y + radius), fill=0)

        # 右侧凹凸
        y = random.randint(height // 4, height * 3 // 4)
        radius = random.randint(5, 10)
        draw.ellipse((width - radius, y - radius, width + radius, y + radius), fill=0)

    return mask


def generate_captcha_image():
    # 获取背景图片（固定400x300尺寸）
    try:
        response = requests.get(BACKGROUND_URL, timeout=5)
        background = Image.open(io.BytesIO(response.content)).convert("RGB")
        background = background.resize((BG_W, BG_H))  # 强制统一尺寸
    except Exception as e:
        background = Image.new('RGB', (BG_W, BG_H), (240, 240, 240))
        print(e)

    bg_width, bg_height = background.size

    # 计算缺口位置（确保在图片范围内）
    gap_x = random.randint(60, bg_width - SLIDER_WIDTH - 10)
    gap_y = random.randint(
        max(GAP_Y_RANGE[0], SLIDER_HEIGHT),
        min(GAP_Y_RANGE[1], bg_height - SLIDER_HEIGHT)
    )

    # 生成缺口遮罩（与滑块同尺寸）
    notch_mask = generate_notch_mask(SLIDER_WIDTH, SLIDER_HEIGHT)

    # 创建滑块图像（从背景精确裁剪）
    slider = Image.new("RGBA", (SLIDER_WIDTH, SLIDER_HEIGHT))
    try:
        slider_bg = background.crop((
            max(0, gap_x),
            max(0, gap_y),
            min(bg_width, gap_x + SLIDER_WIDTH),
            min(bg_height, gap_y + SLIDER_HEIGHT)
        ))
        slider.paste(slider_bg, (0, 0))
    except Exception as e:
        slider_bg = Image.new('RGB', (SLIDER_WIDTH, SLIDER_HEIGHT), (200, 200, 200))
        slider.paste(slider_bg, (0, 0))
        print(e)

    slider.putalpha(notch_mask)

    # 处理背景图（添加缺口效果）
    bg_with_notch = background.copy()

    # 1. 添加缺口阴影
    shadow_layer = Image.new('RGBA', (SLIDER_WIDTH, SLIDER_HEIGHT), (0, 0, 0, 150))
    bg_with_notch.paste(shadow_layer, (gap_x, gap_y), notch_mask)

    # 2. 添加高光边缘
    border = Image.new('RGBA', (SLIDER_WIDTH, SLIDER_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(border)
    draw.rectangle(((0, 0), (SLIDER_WIDTH - 1, SLIDER_HEIGHT - 1)),
                   outline=(0, 0, 0, 0), width=2)
    bg_with_notch.paste(border, (gap_x, gap_y), border)

    # 转换为Base64
    def img_to_base64(img):
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()

    return {
        "bg_base64": img_to_base64(bg_with_notch),
        "slider_base64": img_to_base64(slider),
        "gap_x": gap_x,
        "gap_y": gap_y,
        "slider_width": SLIDER_WIDTH,
        "slider_height": SLIDER_HEIGHT,
        "bg_width": bg_width,
        "bg_height": bg_height
    }


def analyze_trace(trace):
    speeds, accs = [], []
    pauses, reverse_moves = 0, 0
    last_v = None
    init_x = -1
    if len(trace) > 0:
        init_x = trace[0]['x']

    for i in range(1, len(trace)):
        dx = trace[i]['x'] - trace[i - 1]['x']
        dt = trace[i]['t'] - trace[i - 1]['t']
        if dt == 0:
            continue
        v = dx / dt
        speeds.append(v)
        if last_v is not None:
            a = (v - last_v) / dt
            accs.append(a)
            if (v > 0 > last_v) or (v < 0 < last_v):
                reverse_moves += 1
        last_v = v

        if abs(dx) < 1 and dt > 200:
            pauses += 1

    return {
        "mean_speed": sum(speeds) / len(speeds) if speeds else 0,
        "max_speed": max(speeds) if speeds else 0,
        "min_speed": min(speeds) if speeds else 0,
        "mean_acc": sum(accs) / len(accs) if accs else 0,
        "max_acc": max(accs) if accs else 0,
        "min_acc": min(accs) if accs else 0,
        "pauses": pauses,
        "reverse_moves": reverse_moves,
        "trace_points": len(trace),
        "init_x": init_x
    }


def is_human_like(trace_features):
    if trace_features["init_x"] != 0:
        return False
    # 你可以根据业务调整阈值
    if trace_features["trace_points"] < 8:
        return False
    if not (0 <= trace_features["reverse_moves"] <= 3):
        return False
    if not (0 <= trace_features["pauses"] <= 3):
        return False
    if abs(trace_features["mean_speed"]) < 0.05 or abs(trace_features["mean_speed"]) > 1:
        return False
    return True
