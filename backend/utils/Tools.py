import hashlib
import random
import string

import shortuuid


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


def generate_random_recovery_code():
    """
    生成二次验证码的6组恢复码
    """
    arr = []
    for _ in range(6):
        arr.append(generate_random_password(8))
    return arr


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


def count_tokens_messages(messages, model="gpt-3.5-turbo"):
    """
    离线计算 OpenAI 消息的 token 数（适配 gpt-3.5-turbo/gpt-4）
    规则参考 OpenAI 官方文档：https://platform.openai.com/docs/guides/chat/managing-tokens
    """
    # 基础配置（不同模型的基础token开销）
    if model.startswith("gpt-3.5-turbo"):
        # gpt-3.5-turbo-0613 及以上版本规则
        base_per_message = 3
        base_per_name = 1
    elif model.startswith("gpt-4"):
        # gpt-4-0613 及以上版本规则
        base_per_message = 3
        base_per_name = 1
    else:
        # 兼容旧版本/未知模型
        base_per_message = 4
        base_per_name = -1

    num_tokens = 0
    for message in messages:
        # 每个消息的基础开销
        num_tokens += base_per_message
        for key, value in message.items():
            if value is None:
                value = ""
            # 文本转字符串并计算token（按字符≈token的近似规则，精度满足业务）
            # 核心：英文/数字按1字符≈1token，中文按1字≈2token（OpenAI 实际规则）
            str_value = str(value).strip()
            token_count = 0
            for char in str_value:
                if char.isascii():
                    # 英文/数字/符号：1字符=1token
                    token_count += 1
                else:
                    # 中文/多字节字符：1字符≈2token（OpenAI 实际计费规则）
                    token_count += 2
            num_tokens += token_count

            # name字段的额外开销
            if key == "name" and value:
                num_tokens += base_per_name

    # 回复的固定开销（<|end_of_text|>）
    num_tokens += 3
    return num_tokens

#
# # 示例消息列表
# messages = [
#     {"role": "system",
#      "content": "“豆包”这个名字是字节跳动研发团队为我取的。它简单易记、亲切可爱，能方便大家认识和记住我，也让你和我交流时能更自然亲近，你要是喜欢，也可以给我起其他昵称来称呼我呀。 "},
#     {"role": "user", "content": "你为啥叫豆包"}
# ]
#
# token_count = count_tokens_messages(messages)
# print(f"消息列表的 Token 数量: {token_count}")
#
# from dbinfo import DatabaseSession
# from entity import TalkLogs
#
# with DatabaseSession() as session:
#     talk_logs = session.query(TalkLogs).all()
#     for talk_log in talk_logs:
#         messages = [
#             {"role": "system",
#              "content": talk_log.resp_content},
#             {"role": "user", "content": talk_log.req_content}
#         ]
#         # talk_log.tokens = count_tokens_messages(messages)
#         session.query(TalkLogs).filter(TalkLogs.id == talk_log.id).update({TalkLogs.tokens: count_tokens_messages(messages)})
#         session.commit()
#         # session.update(talk_log)
#         # print(talk_log)
#         # DbTools.saveOrUpdate(session, json.dumps(talk_log), TalkLogs)

def generate_custom_id(length=10):
    # 使用自定义字母表生成固定长度的 ID
    alphabet = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    su = shortuuid.ShortUUID(alphabet=alphabet)
    return su.random(length=length)
