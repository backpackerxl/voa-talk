def SuccessReturn(data=None):
    """
    生成成功返回结果
    :param data: 返回的数据
    :return: 成功返回结果
    """
    return {'code': 200, 'data': data, 'msg': "操作成功"}


def ErrorReturn(message, code=400):
    """
    生成错误返回结果
    :param code: 错误码
    :param message: 错误消息
    :return: 错误返回结果
    """
    return {'code': code, 'msg': message}
