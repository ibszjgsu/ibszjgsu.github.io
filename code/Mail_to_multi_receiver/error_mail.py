# -*- coding: utf-8 -*-
"""
Created on Mon May 28 15:12:02 2018

@author: Pikari
"""

import sys
import locale
import poplib
from email import parser
import email
import string

# 确定运行环境的encoding
__g_codeset = sys.getdefaultencoding()
if "ascii"==__g_codeset:
  __g_codeset = locale.getdefaultlocale()[1]

host = 'mail.zjgsu.edu.cn'
username = 'recruit.ibs'
password = '$Ibs11031103'
pop_conn = poplib.POP3_SSL(host)
pop_conn.user(username)
pop_conn.pass_(password)
#Get messages from server:
# 获得邮件
messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]

'''
for j in range(len(messages)):
    for i in range(len(messages[j][1])):
        if messages[j][1][i].decode()[:15] == 'Diagnostic-Code':
            print(messages[j][1][i].decode())
            
'''     

error_554 = 'Diagnostic-Code: SMTP; SMTP error, OPEN: 554'
error_550 = 'Diagnostic-Code: SMTP; SMTP error, RCPT TO: 550'
error_553 = 'Diagnostic-Code: SMTP; SMTP error, RCPT TO: 553'
error_time_out = 'Diagnostic-Code: SMTP; rcpt handle timeout'
error_DNS_query = 'Diagnostic-Code: SMTP; DNS query error'
error = [error_550, error_553, error_554, error_DNS_query, error_time_out]

error_mail = {error_550 : [], 
              error_553 : [], 
              error_554 : [], 
              error_time_out : [], 
              error_DNS_query : []}

for i in range(len(messages)):
    
    #判断邮件是否被退回
    for j in range(len(messages[i][1])):
        if messages[i][1][j].decode()[:15] == 'Diagnostic-Code':
            err = messages[i][1][j].decode()
            
            #错误类型判断
            for error_type in error:
                if err.find(error_type) == 0:
                    break
            
            #查找被退回的邮件地址
            for k in range(len(messages[i][1])):
                if messages[i][1][k].decode()[:12] == 'Delivered-To':
                    mail_address = messages[i][1][k].decode()[14:]
                    mail_address = mail_address[:int(len(mail_address)/2)]
                    error_mail[error_type].append(mail_address)
                    break

print(error_mail)