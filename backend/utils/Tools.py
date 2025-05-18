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


def insert_lowercase_letters(s):
    """
    随机插入字符
    """
    result = s
    # 生成不连续的插入位置
    possible_positions = list(range(len(s) + 1))
    positions = []

    for _ in range(0, 3):
        if not possible_positions:
            break  # 没有可用位置时提前结束
        pos = random.choice(possible_positions)
        positions.append(pos)

        # 移除当前位置及相邻位置
        to_remove = {pos}
        if pos - 1 in possible_positions:
            to_remove.add(pos - 1)
        if pos + 1 in possible_positions:
            to_remove.add(pos + 1)
        possible_positions = [p for p in possible_positions if p not in to_remove]
        # 按位置排序并执行插入
        positions.sort()
        result = s
        offset = 0  # 记录插入导致的位置偏移

        for pos in positions:
            actual_pos = pos + offset
            # 随机决定连续字母数量 (1-3个)
            length = random.randint(1, 3)
            # 仅生成小写字母
            letters = ''.join(random.choices(string.ascii_lowercase, k=length))
            # 执行插入
            result = result[:actual_pos] + letters + result[actual_pos:]
            offset += len(letters)  # 更新偏移量

        # 按位置排序并执行插入
        positions.sort()
        result = s
        offset = 0  # 记录插入导致的位置偏移

        for pos in positions:
            actual_pos = pos + offset
            # 随机决定连续字母数量 (1-3个)
            length = random.randint(1, 3)
            # 仅生成小写字母
            letters = ''.join(random.choices(string.ascii_lowercase, k=length))
            # 执行插入
            result = result[:actual_pos] + letters + result[actual_pos:]
            offset += len(letters)  # 更新偏移量

    return result
