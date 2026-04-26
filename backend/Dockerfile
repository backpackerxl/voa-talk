# 1. 基础镜像：使用官方 Python 轻量级镜像
FROM python:3.10-slim

# 2. 设置工作目录（容器内的路径）
WORKDIR /app

# 3. 复制依赖清单，利用 Docker 缓存加速构建
COPY requirements.txt .

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# 4. 安装依赖（阿里云镜像，加速安装）
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 5. 复制项目所有代码到容器
COPY . .

# 6. 暴露端口（和 Flask 端口一致）
EXPOSE 10011

# 7. 启动命令
CMD ["python", "app.py"]