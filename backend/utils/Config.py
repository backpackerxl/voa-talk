# -*- coding: UTF-8 -*-
import os

# AES的密钥
AesKey = b"hnciquewhngfo1qc"

# JWT的的密钥
SecretKey = 'asgfdgerher'

# 哈希密码
HashingPassword = b'$2b$12$secretsaltsecretsaltse'

# Token的过期时间，单位为天
TheExpirationTimeOfTheToken = 5

# mysql 数据库
# 数据库地址，分本地环境(DEV)/生产环境(PRO)
mysqlAddress = {
    "DEV": "127.0.0.1",
    "PRO": "127.0.0.1"
}
# 数据库端口，分本地环境(DEV)/生产环境(PRO)
mysqlPort = {
    "DEV": 3306,
    "PRO": 3308
}
# 数据库用户名
mysqlUser = "root"
# 数据库密码
mysqlPWD = os.getenv('MYSQL_PASSWORD')

# Rides数据库
# 链接地址，分本地环境(DEV)/生产环境(PRO)
ridesAddress = {
    "DEV": "127.0.0.1",
    "PRO": "127.0.0.1"
}
# Rides，端口，分本地环境(DEV)/生产环境(PRO)
ridesPort = {
    "DEV": 6379,
    "PRO": 6379
}
# Rides，密码
ridesPassword = None
# Rides，数据库
ridesDb = 0

# 分页查询的默认页数
PageSize = 20
# 分页查询的最大页数
MaxPageSize = 99999999
# 分页查询的默认页码
PageIndex = 1

# 你的SMTP服务器地址
SMTP_SERVER = "smtp.exmail.qq.com"
# 你的SMTP服务器端口
SMTP_PORT = 465
# 你的企业邮箱登录用户名
EMAIL_USER = "voatalk@voatalk.online"
# email授权码
EMAIL_CODE = os.getenv('EMAIL_PASSWORD')
