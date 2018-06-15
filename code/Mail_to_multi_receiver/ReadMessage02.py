# -*- coding: utf-8 -*-
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import poplib
host = 'mail.zjgsu.edu.cn'
username = 'recruit.ibs'
password = '$Ibs11031103'
pop_conn = poplib.POP3_SSL(host)
pop_conn.user(username)
pop_conn.pass_(password)
pop_conn.set_debuglevel(1)
resp, mails, octets = pop_conn.list()
index = len(mails)
#index = 0
resp, lines, octets = pop_conn.retr(index)
# lines存储了邮件的原始文本的每一行,
# 可以获得整个邮件的原始文本:
msg_content = b'\r\n'.join(lines).decode('utf-8')

# 稍后解析出邮件:
msg = Parser().parsestr(msg_content)


