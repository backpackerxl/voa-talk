# -*- coding: UTF-8 -*-

import importlib
import os
import pkgutil

import waitress
from datetime import date
from pathlib import Path
from flask import Flask, Blueprint, send_from_directory, request
from flask_cors import CORS

from utils.GetChatId import Snowflake
from utils.JwtUtils import token_on

app = Flask(__name__)
snowflake = Snowflake(data_center_id=1, worker_id=1)

CORS(app, supports_credentials=True)


@app.route('/')
def hello():
    return '你走错地方了，这里是后端。'


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
@token_on
def upload_file():
    # 检查请求中是否有文件
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400
    file = request.files['file']
    # 检查文件名是否为空
    if file.filename == '':
        return {'error': 'No selected file'}, 400
    # 检查文件扩展名是否允许
    if file and allowed_file(file.filename):
        # 获取今天的日期并格式化为 YYYYMMDD
        today = date.today().strftime('%Y%m%d')
        # 创建按日期划分的子目录
        date_folder = Path(app.config['UPLOAD_FOLDER']) / today
        os.makedirs(date_folder, exist_ok=True)  # 自动创建目录(如果不存在)
        # 获取文件扩展名
        file_ext = os.path.splitext(file.filename)[1]
        # 生成唯一的文件名
        new_filename = str(snowflake.next_id()) + file_ext
        save_path = date_folder / new_filename
        file.save(save_path)
        # 返回可访问的图片地址
        image_url = f'/uploads/{today}/{new_filename}'
        return {'image_url': image_url}, 200
    return {'error': 'Invalid file type'}, 400


@app.route('/uploads/<path:file_path>')
def uploaded_file(file_path):
    # 分离目录和文件名
    directory, filename = os.path.split(file_path)
    # 构建完整的目录路径
    full_directory = Path(app.config['UPLOAD_FOLDER']) / directory
    # 发送文件
    return send_from_directory(full_directory, filename)


# 获取当前文件所在目录的绝对路径
base_dir = os.path.abspath(os.path.dirname(__file__))
# 将蓝图文件夹的相对路径转为绝对路径
blueprints_dir = os.path.join(base_dir, 'blueprints')


# pip install pyjwt  -i https://pypi.tuna.tsinghua.edu.cn/simple/
def register_blueprints(app: Flask, package_name: str, package_path: str):
    """
    自动注册指定包中的所有蓝图

    :param app: Flask应用实例
    :param package_name: 蓝图包的名称
    :param package_path: 蓝图包的路径
    """
    # 遍历指定路径中的所有模块
    for _, module_name, _ in pkgutil.iter_modules([package_path]):
        # 动态导入模块
        module = importlib.import_module(f"{package_name}.{module_name}")
        # 遍历模块中的所有属性
        for attr in dir(module):
            attr_value = getattr(module, attr)
            # 如果属性是一个Blueprint实例，注册到Flask应用
            if isinstance(attr_value, Blueprint):
                app.register_blueprint(attr_value, url_prefix=f'/{attr_value.name}')


# 注册所有蓝图
register_blueprints(app, 'blueprints', blueprints_dir)

if __name__ == '__main__':
    print("启动服务器 http://localhost:10011")
    try:
        waitress.serve(app,
                       host='0.0.0.0',
                       port=10011
                       )
    except Exception as e:
        print(f"启动服务器失败：{e}")
