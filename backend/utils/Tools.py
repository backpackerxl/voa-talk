import hashlib
import random
import string


def generate_random_password(length=8):
    """
    生成指定长度的随机密码
    """
    # 确保密码长度至少为4，以包含各种字符类型的混合
    if length < 4:
        raise ValueError("密码长度应至少为4以确保字符类型的混合。")

    # 确保密码包含至少一个大写字母、一个小写字母和一个数字
    password = [
        random.choice(string.ascii_uppercase),  # 至少一个大写字母
        random.choice(string.ascii_lowercase),  # 至少一个小写字母
        random.choice(string.digits),  # 至少一个数字
    ]

    # 从所有允许的字符中随机选择，填充密码的其余长度
    all_characters = string.ascii_letters + string.digits
    password.extend(random.choice(all_characters) for _ in range(length - 3))

    # 打乱密码以确保随机性，然后将其连接成一个字符串
    random.shuffle(password)
    return ''.join(password)


def generate_hashed_password(password):
    """
    生成哈希密码
    :param password:  原始密码
    :return:  哈希密码和盐
    """
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    return hashlib.sha256((password + salt).encode()).hexdigest(), salt
