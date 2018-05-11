# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 23:15:52 2018

@author: Administrator
"""

import smtplib  
from email.mime.text import MIMEText  
import os
import re
import mysql.connector
# import csv

def table_exist(tab_name):
    cur.execute('show tables')  # 罗列所有当前库里面的所有表格
    tables = cur.fetchall()
    selectab = re.compile(r'\w*\w*')
    tabnames = selectab.findall(str(tables))
    res = tab_name in tabnames
    return res


########
  
#mail_host="smtp.163.com"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址  
#mail_user="xinihe"                           #用户名  
#mail_pass=input('Please enter the password of the sending mailbox:')                          #密码  
#mail_postfix="163.com"                     #邮箱的后缀，网易就是163.com  

#==============================================================================
# 
# mail_host="mail.zjgsu.edu.cn"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址  
# mail_user="ibs.recurit"                           #用户名  
# mail_pass=input('Please enter the password of the sending mailbox:')     #密码  
# mail_postfix="zjgsu.edu.cn"                     #邮箱的后缀，网易就是163.com
# 
#==============================================================================

#######
#==============================================================================
# 
# 
# def send_mail(to_list,sub,content):  
#     me="Mail from IBS"+"<"+mail_user+"@"+mail_postfix+">"  
#     msg = MIMEText(content,_subtype='plain')  
#     msg['Subject'] = sub  
#     msg['From'] = me  
#     msg['To'] = to_list                #将收件人列表以‘；’分隔  
#     try:  
#         server = smtplib.SMTP()  
#         server.connect(mail_host, 25)                            #连接服务器  
#         server.login(mail_user,mail_pass)               #登录操作  
#         server.sendmail(me, to_list, msg.as_string())  
#         server.close()  
#         return True  
#     except: 
#         return False  
# 
# f = open(os.getcwd()+'\\content.txt','r')  # 读取正文内容
# mailcontent = f.read()
# f.close()
# 
# f = open(os.getcwd()+'\\sub.txt','r') # 读取邮件主题
# mailsub = f.read()
# f.close()
# 
#==============================================================================
'''
Load information from CSV files
'''
#mailto_list = []
#rec_name = []
#rec_article = []
#f = csv.reader(open(os.getcwd()+'\\namelist.csv')) # 读取收件人 邮箱和姓名信息
#for rows in f:
#    mailto_list.append(rows[2])
#    rec_name.append(rows[0])
#    rec_article.append(rows[3])
#    
#mailto_list.pop(0) # 删除行号
#rec_name.pop(0)
#rec_article.pop(0)

#找到收件人，然后检索是否发送过邮件
    

'''
Use information from Database and update another table
'''
conn = mysql.connector.connect(host="10.23.0.2",port=3306,user="root",\
                       password= '11031103',database="journalcontact",charset="utf8")
cur = conn.cursor()

if not table_exist('rec_email2'):
    #build a new table named by the journal title 
    sql_new = "create table rec_email2 (id int not null unique auto_increment, author varchar(100) Null,"
    sql_new+="email varchar(100) Null,"
    sql_new+="sent int Null,"
    sql_new+="confidence varchar(100) Null,"
    sql_new+="cn varchar(100) Null,"
    sql_new+="country varchar(100) Null,"
    sql_new+="journal varchar(100) Null,"
    sql_new+="citation varchar(100) Null,"
    sql_new+="volume varchar(100) Null,"
    sql_new+="year varchar(100) Null,"
    sql_new+="title varchar(1000) Null,"
    sql_new+="url varchar(1000) Null,"
    sql_new+="primary key(id))"
    # Design the table  No. 1
    cur.execute(sql_new)
    conn.commit()

sql_select = "select * from email_jour_auth3"
cur.execute(sql_select)
info = cur.fetchall()


idcnt =1 
for i in range(len(info)):
#==============================================================================
#     modifiedcontent = mailcontent.split('XXX')[0] + info[i][11].split('\'')[1] + mailcontent.split('XXX')[1]
#     content = 'Dear' + info[i][1].split('\'')[1]+'\n' + modifiedcontent                         #发送1封，上面的列表是几个人，这个就填几  
#    
#==============================================================================
    # Check if the author has been in touched (No. 2)
    now_name = info[i][1].split('\'')[1]

    sql_select = "select * from rec_email2"
    cur.execute(sql_select)
    rec_info = cur.fetchall()
    sql_find = 'select * from rec_email2 where author=\"%s\"'%now_name
    cur.execute(sql_find)
    cnt = cur.fetchone()
    if(cnt == None):     #若未发送过邮件
        #将该作者信息添加到已发送表格中
       
#==============================================================================
# #==============================================================================
# #         if send_mail(info[i][2].split('\'')[1],mailsub,content):  #邮件主题和邮件内容  
# #             #这是最好写点中文，如果随便写，可能会被网易当做垃圾邮件退信  
# #             print("Mail sent to "+info[i][2].split('\'')[1]+' successfully!')  
#                # update the table  No. 3
#              sql_add = "insert into rec_email2(id,author,email,sent,title)values("
#              sql_add+="\"%s\","%str(idcnt)
#              idcnt+=1
#              sql_add+="\"%s\","%info[i][1].split('\'')[1]
#              sql_add+="\"%s\","%info[i][2].split('\'')[1]
#              sql_add+="\"1\","
#              sql_add+="\"%s\")"%info[i][11].split('\'')[1]
#              cur.execute(sql_add)
# #         else:  
# #             print("failed to be received by "+info[i][2].split('\'')[1]+'!')  
# #==============================================================================
#       
#==============================================================================
        conn.commit()