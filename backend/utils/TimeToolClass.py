# -*- coding: utf-8 -*-
# @Author : Liu宗鑫
# @Time : 2024/6/6 上午10:56
# @File : TimeToolClass.py
# @Software: PyCharm
def get_time(date_format='%Y-%m-%d %H:%M:%S'):
    """
    获取当前年月日%Y-%m-%d %H:%M:%S格式 或者%Y-%m-%d 。
    :param date_format: 日期格式 ，如 '%Y-%m-%d' 或 '%Y-%m-%d %H:%M:%S'
    :return:
    """
    import datetime
    return datetime.datetime.now().strftime(date_format)
