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
import mysql.connector
from datetime import datetime

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

#连接数据库
conn = mysql.connector.connect(host="10.23.0.2",port=3306,user="root",\
                       password= '11031103',database="journalcontact",charset="utf8")
cur = conn.cursor()

for i in range(len(messages)):
    
    #判断邮件是否被退回
    for j in range(len(messages[i][1])):
        if messages[i][1][j].decode()[:15] == 'Diagnostic-Code':
            err = messages[i][1][j].decode()
             
			  #标记错误是否为550
            flag_550 = 0
			
            #错误类型判断
            for error_type in error:
                if err.find(error_type) == 0:
                    if(error_type == error_550):
                        flag_550 = 1
                    break
            
            #获取拒收邮件时间
            for k in range(len(messages[i][1])):
                if messages[i][1][k].decode()[:4] == 'Date':
                    mail_time = messages[i][1][k].decode()[:45]
                    mail_time = mail_time[6:]
                    mail_time = datetime.strptime(mail_time[5:25],'%d %b %Y %H:%M:%S')
                    error_mail[error_type].append(mail_time)
                    break
            #查找被退回的邮件地址        
            for k in range(len(messages[i][1])):
                if messages[i][1][k].decode()[:12] == 'Delivered-To':
                    mail_address = messages[i][1][k].decode()[14:]
                    mail_address = mail_address[:int(len(mail_address)/2)]
                    error_mail[error_type].append(mail_address)
                    if(flag_550==1):#标记550错误的邮箱地址
                        sql_update='update all_info set fail_550 = "1" where email = %s '
                        cont_ins = [mail_address]
                        cur.execute(sql_update,cont_ins);
                        conn.commit();
                    break
#输出到data文件中   
fw=open('data.doc','w')
for i in range(len(error)):   
    #输出错误类型及对应数量
    fw.write('{ee}: num({num})\n'.format(num = (int)(len(error_mail[error[i]])/2),ee = error[i]))
    for j in range(len(error_mail[error[i]])-1):
       if j%2==1:
           continue
       fw.write('  {ertime}'.format(ertime = error_mail[error[i]][j]) +':  '+ error_mail[error[i]][j+1]+'\n')
    fw.write('\n')
fw.close()
        



