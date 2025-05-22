# VoaTalk

## git clone project

```commandline
git clone https://github.com/backpackerxl/voa-talk.git
```

## Frontend Project setup

```commandline
cd frontend
```

```
npm install
```

### Compiles and hot-reloads for development

```
npm run serve
```

### Compiles and minifies for production

```
npm run build
```

## Backend Project setup

```commandline
cd backend
```

```commandline
mkdir logfile uploads
```

```
pip install -r requirements.txt
```

### Compiles and hot-reloads for development

```
python app.py
```

### Mail setting
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
