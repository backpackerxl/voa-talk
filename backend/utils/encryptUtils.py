# -*- coding: utf-8 -*-
# @Author : Liu宗鑫
# @Time : 2024/8/9 下午4:34
# @File : encryptUtils.py
# @Software: PyCharm
import base64

from Crypto.Cipher import AES

from utils import Config


def encrypt_aes(plaintext):
    """
    使用AES加密文本
    :param plaintext:
    :return:
    """
    key = Config.AesKey
    cipher = AES.new(key, AES.MODE_CBC, iv=b'\x00' * 16)
    plaintext_bytes = plaintext.encode('utf-8') + b'\x00' * (16 - len(plaintext) % 16)
    ciphertext_bytes = cipher.encrypt(plaintext_bytes)
    return base64.b64encode(ciphertext_bytes).decode('utf-8')


def aes_decrypt(ciphertext):
    '''
    解密AES文本
    '''
    # 将密钥和初始化向量转换为字节类型
    key = Config.AesKey
    # 将 Base64 编码的密文解码为字节类型
    ciphertext = base64.b64decode(ciphertext)
    # 创建 AES 解密器对象
    cipher = AES.new(key, AES.MODE_CBC, iv=b'\x00' * 16)
    # 解密数据
    decrypted_data = cipher.decrypt(ciphertext).rstrip(b'\x00')
    # 将解密后的字节数据转换为字符串
    return decrypted_data.decode('utf-8')
