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
import time
import csv

def table_exist(tab_name):
    cur.execute('show tables')  # 罗列所有当前库里面的所有表格
    tables = cur.fetchall()
    selectab = re.compile(r'\w*\w*')
    tabnames = selectab.findall(str(tables))
    res = tab_name in tabnames
    return res


#==============================================================================
  
#mail_host="smtp.163.com"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址  
#mail_user="xinihe"                           #用户名  
#mail_pass=input('Please enter the password of the sending mailbox:')                          #密码  
#mail_postfix="163.com"                     #邮箱的后缀，网易就是163.com  

#==============================================================================
 
mail_host="mail.zjgsu.edu.cn"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址  
mail_user="recruit.ibs"                           #用户名  
mail_pass="$Ibs11031103"     #密码  
mail_postfix="zjgsu.edu.cn"                     #邮箱的后缀，网易就是163.com
 
#==============================================================================

# 
def send_mail(to_list,sub,content):  
    me="International Business School in Zhejiang Gongshang Univ "+"<"+mail_user+"@"+mail_postfix+">"  
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
    
#==============================================================================

f = open(os.getcwd()+'\\phdcontent.txt','r')  # 读取正文内容
mailcontent = f.read()
f.close()
 
f = open(os.getcwd()+'\\sub.txt','r') # 读取邮件主题
mailsub = f.read()
f.close()

# Log
flog = open(os.getcwd() + '\\log.txt', 'a+')  # 读取日志内容
flog.writelines('\n \n Date Updating Log on ' + time.strftime('%Y-%m-%d',time.localtime(time.time())) + '\n')
flog.writelines('Start from: '+ time.strftime('%H:%M:%S',time.localtime(time.time())) + '\n')
# 
#==============================================================================

'''
Use information from Database and update another table
'''
conn = mysql.connector.connect(host="10.23.0.2",port=3306,user="root",\
                       password= '11031103',database="journalcontact",charset="utf8")
cur = conn.cursor()

if not table_exist('rec_email_univ'):
    #build a new table named by the journal title 
    sql_new = "create table rec_email_univ (id int not null unique auto_increment, name varchar(100) Null,"
    sql_new+="email varchar(100) Null,"
    sql_new+="response int Null,"
    sql_new+="country varchar(500) Null,"
    sql_new+="university varchar(500) Null,"
    sql_new+="major varchar(1000) Null,"
    sql_new+="year varchar(100) Null,"
    sql_new+="attempt varchar(1000) Null,"
    sql_new+="primary key(id))"
    cur.execute(sql_new)
    conn.commit()
#==============================================================================

'''
Load information from CSV files
'''
mailto_list = []
rec_name = []
rec_univ = []
rec_major = []
f = csv.reader(open(os.getcwd()+'\\namelist.csv')) # 读取收件人 邮箱和姓名信息
for rows in f:
    mailto_list.append(rows[1])
    rec_name.append(rows[0])
    rec_univ.append(rows[5])
    rec_major.append(rows[6])
#    
mailto_list.pop(0) # 删除行号
rec_name.pop(0)
rec_univ.pop(0)
rec_major.pop(0)

#找到收件人，然后检索是否发送过邮件

    



#sql_select = "select * from email_jour_auth3"
#cur.execute(sql_select)
#info = cur.fetchall()

#=======================

suc = 0
fails = 0
for i in range(len(rec_name)):
    
    content = mailcontent.split('XXX')[0] + rec_name[i].split(' ')[-1] + mailcontent.split('XXX')[1]
#    content = 'Dear Dr. ' + rec_name[i].split(' ')[-1]+'\n' + mailcontent                         #发送1封，上面的列表是几个人，这个就填几  
    
    # Check if the author has been in touched (No. 2)
    receiver = rec_name[i].split(' ')[-1] + ',' + rec_name[i].split(' ')[:-1][0]
#    now_name = info[i][1].split('\'')[1]

#    sql_select = "select * from rec_email2"
#    cur.execute(sql_select)
#    rec_info = cur.fetchall()
    sql_find = 'select * from rec_email_univ where rec_email_univ.name=\"%s\"'%receiver
#    sql_find = 'select * from rec_email3, rec_email_univ where rec_email3.author= %s or rec_email_univ.name= %s'
#    cur.execute(sql_find, (receiver, receiver))
    cur.execute(sql_find)
    cnt = cur.fetchone()
    time.sleep(3)#睡眠2秒 
    if(cnt == None):     #若未发送过邮件
        #将该作者信息添加到已发送表格中
        if send_mail(mailto_list[i],mailsub,content):
            print("Mail sent to "+mailto_list[i]+' successfully!')
            suc = suc + 1
              
        # update the table  No. 3
            sql_add = "insert into rec_email_univ(name,email,university,attempt)values("
            sql_add+="\"%s\","%receiver  # author name
            sql_add+="\"%s\","%mailto_list[i]  # email address
#            sql_add+="\"1\","  # Num of attempts
            sql_add+="\"%s\","%rec_univ[i] #university
#            sql_add+="\"%s\","%rec_major[i]   #  major
#            sql_add+="\"%s\","%info[i][6].split('\'')[1]   # country
#            sql_add+="\"%s\","%info[i][7].split('\'')[1]   #  journal   
#            sql_add+="\"%s\","%info[i][8].split('\'')[1]   #  citation
#            sql_add+="\"%s\","%info[i][9].split('\'')[1]   #  volume
#            sql_add+="\"%s\","%info[i][10].split('\'')[1]  #  year
#            sql_add+="\"%s\","%info[i][11].split('\'')[1]  #  title
            sql_add+="\"%s\")"%time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))   #  last attempt date
            cur.execute(sql_add)
            conn.commit()
        else:  
            print("failed to be received by "+mailto_list[i]+'!')
            fails = fails + 1
            flog.writelines('failed to be received by '+mailto_list[i]+'!' + '\n')
# #==============================================================================
flog.writelines('In total, there is '+ str(suc) + ' messages has been sent successfully while ' +str(fails)+ ' messages can not be sent. \n')
flog.writelines('End at: '+ time.strftime('%H:%M:%S',time.localtime(time.time())) + '\n')
#send_mail('ibs@zjgsu.edu.cn','Mail Log', flog.read())   
flog.close()   
#==============================================================================
        