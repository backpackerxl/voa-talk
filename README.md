<div style="text-align: center;">
    <img src="frontend/src/assets/images/logo.png" alt="图片描述">
</div>

# How to Use

## 1.git clone project

```commandline
git clone https://github.com/backpackerxl/voa-talk.git
```

## 2.Frontend Project setup

```commandline
cd frontend
```

```
npm install
```

### 2.1Compiles and hot-reloads for development

```
npm run serve
```

### 2.2Compiles and minifies for production

```
npm run build
```

## 3.Backend Project setup

```commandline
cd backend
```

```commandline
mkdir logfile uploads
```

```
pip install -r requirements.txt
```

### 3.1Compiles and hot-reloads for development

```
python app.py
```

### 3.2Mail setting

- individual mail setting
- set `Config.py`

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
