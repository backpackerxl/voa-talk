import base64
import json

import redis

from utils import Config


class RedisHandler:
    def __init__(self):
        # 构建参数字典
        pool_kwargs = {
            'host': Config.ridesAddress,
            'port': Config.ridesPort,
            'decode_responses': True
        }

        # 如果有密码，才添加到参数字典中
        if Config.ridesPassword:
            pool_kwargs['password'] = Config.ridesPassword

        # 创建连接池
        self.pool = redis.ConnectionPool(**pool_kwargs)
        # 使用连接池创建Redis对象
        self.rd = redis.Redis(connection_pool=self.pool)

    def save_code(self, code, cache_duration):
        '''
        把临时生成的验证码存储到redis
        '''
        self.rd.set('code_' + code, code)  # 把验证码存储起来
        self.rd.expire('code_' + code, cache_duration)  # 验证码 5分钟后时效

    def save_key(self, key, value, cache_duration):
        '''
        存储普通键只对
        '''
        self.rd.set(key, value)
        self.rd.expire(key, cache_duration)

    def get_key(self, key):
        '''
        获取值
        '''
        return self.rd.get(key)

    def check_code(self, code):
        """
        检测验证码是否过期：用于登录或者前端验证使用
        :param code:
        :return:
        """
        code = encrypt(code.lower())
        if not self.rd.get('code_' + code):
            return False
        return True


# 加密（编码）函数
def encrypt(plaintext):
    """
    加密（编码）函数
    :param plaintext:
    :return:
    """
    encoded_bytes = base64.b64encode(plaintext.encode("utf-8"))
    encoded_str = encoded_bytes.decode("utf-8")
    return encoded_str


class RedisKeyValueStore:
    def __init__(self):
        self.client = redis.Redis(host=Config.ridesAddress, port=Config.ridesPort, db=Config.ridesDb)

    def add_or_update(self, key, value):
        """
        添加或更新键值对。
        如果键已存在，则更新其值；如果键不存在，则添加键值对。
        """
        self.client.set(key, value)

    def query(self, key):
        """
        根据键查询值。
        如果键存在，返回对应的值；如果键不存在，返回None。
        """
        value = self.client.get(key)
        if value is not None:
            return value.decode('utf-8')
        return None


if __name__ == '__main__':
    # 使用方式：
    RedisHandler().save_code("D8UXBN", 60)  # 保存验证码 ，60秒后过期
    print(RedisHandler().check_code("D8UXBN", ))  # 检查验证码是否过期 ，过期返回False，未过期返回True
    dict_user = {
        "username": "bxl",
        "email": "946113@qq.com"
    }
    RedisHandler().save_key('66a19a88-eaa3-434a-ba06-4a984fcc4981', json.dumps(dict_user), 300)
    print(RedisHandler().get_key('66a19a88-eaa3-434a-ba06-4a984fcc4981'))
