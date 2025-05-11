# 读取ini文件
import configparser
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utils import Config


def send_email(to_email, subject, body, is_html=False):
    """
    发送电子邮件的函数，使用邮箱进行信息的发送
    :param to_email: 收件人的电子邮件地址
    :param subject: 邮件的主题
    :param body: 邮件的正文
    :param is_html:  正文是否是HTML格式，如果为False，则为纯文本
    :return:
    """

    msg = MIMEMultipart()  # 创建一个 multipart 电子邮件消息
    msg['From'] = Config.EMAIL_USER
    msg['To'] = to_email  # 收件人地址
    msg['Subject'] = subject  # 邮件主题

    msg.attach(MIMEText(body, 'html' if is_html else 'plain'))  # 创建邮件正文

    # 连接到你的企业SMTP服务器
    try:
        server = smtplib.SMTP_SSL(Config.SMTP_SERVER, int(Config.SMTP_PORT))  # 使用 SMTP_SSL 而不是 SMTP
        server.login(Config.EMAIL_USER, os.getenv('EMAIL_PASSWORD'))

        # 发送电子邮件
        server.sendmail(Config.EMAIL_USER, [to_email], msg.as_string())
        server.close()

        return '电子邮件发送成功！'
    except Exception as e:
        return f'发送电子邮件失败：{str(e)}'


# 用法示例
if __name__ == '__main__':
    result_msg = send_email('946115360@qq.com', 'Python电子邮件测试2', '这是一封从Python发送的测试电子邮件。')
    print(result_msg)
