a#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import parseaddr, formataddr
# 格式化邮件地址
#def formatAddr(s):
#    name, addr = parseaddr(s)
#    return formataddr((Header(name, 'utf-8'), addr))
def sendMail(sub, body, image = []):
    smtp_server = 'smtp.163.com'
    from_mail = 'xinihe@163.com'
    mail_postfix="163.com" 
    mail_pass = input('Please enter the password of your SMTP account:')
    to_mail = ['ni.he@qq.com', 'xinihe@163.com']
    me="Mail from IBS"+"<"+from_mail+"@"+mail_postfix+">"  
    # 构造一个MIMEMultipart对象代表邮件本身
    msg = MIMEMultipart() 
    # Header对中文进行转码
    msg['From'] = me
    msg['To'] = ','.join(to_mail)
    msg['Subject'] = sub
    msg.attach(MIMEText(body, 'html'))
    # 二进制模式读取图片
    if not image  == []:
        with open(image, 'rb') as f:
            msgImage = MIMEImage(f.read())
        # 定义图片ID
        msgImage.add_header('Content-ID', '<image1>')
        msg.attach(msgImage)
    try:
        s = smtplib.SMTP()     
        s.connect(smtp_server, "25")   
        s.login(from_mail, mail_pass)
        s.sendmail(from_mail, to_mail, msg.as_string())  # as_string()把MIMEText对象变成str     
        s.quit()
    except smtplib.SMTPException as e:
        print("Error: %s" % e)
        
if __name__ == "__main__":
    body = """
    <p>Python 邮件发送测试...</p>
    <h1>测试图片</h1>
    <img src="cid:image1"/>    # 引用图片
    """
    image = 'G:\亿方云\FangCloudSync\浙江工商大学国际商学院\Git\ibszjgsu.github.io\code\Mail_to_multi_receiver\logo.gif'
    sub = 'Test Mail'
    sendMail(sub,body)