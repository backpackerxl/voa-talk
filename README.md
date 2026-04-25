<div style="text-align: center;">
    <img src="frontend/src/assets/images/logo.png" alt="图片描述">
</div>

# How to Use

## 1.git clone project

```shell
git clone https://github.com/backpackerxl/voa-talk.git
```

## 2.Frontend Project setup

```shell
cd frontend
```

```shell
npm install
```

### 2.1Compiles and hot-reloads for development

```shell
npm run dev
```

### 2.2Compiles and minifies for production

```shell
npm run build
```

## 3.Backend Project setup

更新依赖

```shell
pip freeze > requirements.txt
```

### 管理员账号密码

- 账号：admin
- 密码：123456

### 无docker启动/部署方式

> 这种方式需要自行安装依赖、mysql数据库、redis数据库、且配置多而繁杂的环境变量

```commandline
EMAIL_PASSWORD=xxxx;
GITHUB_CLIENT_SECRET=xxx;
MYSQL_DATABASE=ai_chat;
MYSQL_IP=127.0.0.1;
MYSQL_PASSWORD=xxxx;
MYSQL_PORT=3306;
QQ_CLIENT_SECRET=xxxx;
REDIS_IP=127.0.0.1;
REDIS_PORT=6379
```

```commandline
cd backend
```

```commandline
mkdir logfile uploads
```

```shell
pip install -r requirements.txt
```

### 3.1Compiles and hot-reloads for development

```
python app.py
```

### 3.2Mail setting

- individual mail setting
- set `Config.py`

- 第三方邮件服务配置示例

```python
# 你的SMTP服务器地址
SMTP_SERVER = "smtp.163.com"
# 你的SMTP服务器端口
SMTP_PORT = 465
# 你的企业邮箱登录用户名
EMAIL_USER = "xxxx"
# 登录密码，或者授权密码设置为环境变量
EMAIL_PASSWORD = "xxx"
```

#### docker 部署方式(推荐)

> 准备环境变量

```commandline
EMAIL_PASSWORD=xxxx;
GITHUB_CLIENT_SECRET=xxx;
MYSQL_PASSWORD=xxxx;
QQ_CLIENT_SECRET=xxxx;
```

```shell
# 检查环境
docker compose config
# 启动服务
docker compose up -d
```