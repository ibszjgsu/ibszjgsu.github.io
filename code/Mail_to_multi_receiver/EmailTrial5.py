# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 23:15:52 2018

@author: Administrator
"""

import smtplib  
from email.mime.text import MIMEText  
import os
import csv

def send_mail(to_list,sub,content):  
    me="Mail from IBS"+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = to_list                #将收件人列表以‘；’分隔  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host, 25)                            #连接服务器  
        server.login(mail_user,mail_pass)               #登录操作  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except: 
        return False  

f = open(os.getcwd()+'\\content.txt','r')  # 读取正文内容
mailcontent = f.read()
f.close()

f = open(os.getcwd()+'\\sub.txt','r') # 读取邮件主题
mailsub = f.read()
f.close()

mailto_list = []
rec_name = []
f = csv.reader(open(os.getcwd()+'\\namelist.csv')) # 读取收件人 邮箱和姓名信息
for rows in f:
    mailto_list.append(rows[2])
    rec_name.append(rows[0])
    
mailto_list.pop(0) # 删除行号
rec_name.pop(0)

########
  
#mail_host="smtp.163.com"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址  
#mail_user="xinihe"                           #用户名  
#mail_pass=input('Please enter the password of the sending mailbox:')                          #密码  
#mail_postfix="163.com"                     #邮箱的后缀，网易就是163.com  


mail_host="mail.zjgsu.edu.cn"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址  
mail_user="nihe"                           #用户名  
mail_pass=input('Please enter the password of the sending mailbox:')     #密码  
mail_postfix="zjgsu.edu.cn"                     #邮箱的后缀，网易就是163.com


#######
for i in range(len(mailto_list)):
    content = '尊敬的' + rec_name[i]+'\n\n' + mailcontent                         #发送1封，上面的列表是几个人，这个就填几  
    if send_mail(mailto_list[i],mailsub,content):  #邮件主题和邮件内容  
            #这是最好写点中文，如果随便写，可能会被网易当做垃圾邮件退信  
        print("Mail sent to "+mailto_list[i]+' successfully!')  
    else:  
        print("failed to be received by "+mailto_list[i]+'!')  