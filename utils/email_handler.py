from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from django_demo import settings, logger
from django.core.mail import send_mail

class EmailHandler(object):

    """
    Email处理类
    """

    # qq邮箱smtp服务器
    host_server = 'smtp.qq.com'

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.sender = settings.EMAIL_SENDER
        self.sender_pwd = settings.EMAIL_SENDER_pwd
        self.smtp = SMTP_SSL(self.host_server)
        # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
        self.smtp.set_debuglevel(1)
        self.smtp.ehlo(self.host_server)
        self.smtp.login(self.sender, self.sender_pwd)

    def send_mail(self,receiver_list:list, mail_title:str, mail_content:str):
        """
        发送邮件
        :param receiver:
        :param mail_title:
        :param mail_content:
        :return:
        """
        try:
            msg = MIMEText(mail_content, "plain", 'utf-8')
            msg["Subject"] = Header(mail_title, 'utf-8')
            msg["From"] = self.sender
            msg['To'] = ','.join(receiver_list)  # 收件人，必须是一个字符串
            self.smtp.sendmail(self.sender, receiver_list, msg.as_string())
        except Exception as ex:
            logger.error("Send email receiver={0} error by {1}".format(receiver_list,ex))

    def __del__(self):
        self.smtp.quit()

def django_send_email(username, token,receiver):
    """
    发送注册邮件
    :param username:
    :param token:
    :param receiver:
    :return:
    """
    try:
        subject = "django_demo用户激活邮件"  # 邮件标题
        body = ""  # 邮件体
        sender = settings.EMAIL_FROM  # 发件人
        receivers = [receiver]  # 接收人
        html_body = '<h1>尊敬的用户 %s, 感谢您注册django_demo！</h1>' \
                    '<br/><p>请点击此链接激活您的帐号<a href="http://127.0.0.1:8000/user/active/%s">' \
                    'http://127.0.0.1:8000/user/active/%s<a></p>' % (username, token, token)  # html邮件体
        send_mail(subject, body, sender, receivers, html_message=html_body)
    except Exception as ex:
        raise ex
