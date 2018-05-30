

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
# 
# mail_host="mail.zjgsu.edu.cn"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址  
# 
# mail_user="recruit.ibs"                           #用户名  
# 
# mail_pass=input('Please enter the password of the sending mailbox:')     #密码  
# 
# mail_postfix="zjgsu.edu.cn"                     #邮箱的后缀，网易就是163.com
# 
#  
# 
# 
# 
# 
# def send_mail(to_list,sub,content):  
# 
#     me="International Business School in Zhejiang Gongshang Univ "+"<"+mail_user+"@"+mail_postfix+">"  
# 
#     msg = MIMEText(content,_subtype='plain')  
# 
#     msg['Subject'] = sub  
# 
#     msg['From'] = me  
# 
#     msg['To'] = to_list                #将收件人列表以‘；’分隔  
# 
#     try:  
# 
#         server = smtplib.SMTP()  
# 
#         server.connect(mail_host, 25)                            #连接服务器  
# 
#         server.login(mail_user,mail_pass)               #登录操作  
# 
#         server.sendmail(me, to_list, msg.as_string())  
# 
#         server.close()  
# 
#         return True  
# 
#     except: 
# 
#         return False  
# 
#  
# 
# f = open(os.getcwd()+'\\content.txt','r')  # 读取正文内容
# 
# mailcontent = f.read()
# 
# f.close()
# 
#  
# 
# f = open(os.getcwd()+'\\sub.txt','r') # 读取邮件主题
# 
# mailsub = f.read()
# 
# f.close()
# 
# 
# 
# # Log
# 
# flog = open(os.getcwd() + '\\log.txt', 'a+')  # 读取日志内容
# 
# flog.writelines('\n \n Date Updating Log on ' + time.strftime('%Y-%m-%d',time.localtime(time.time())) + '\n')
# 
# flog.writelines('Start from: '+ time.strftime('%H:%M:%S',time.localtime(time.time())) + '\n')
# 
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



if not table_exist('rec_email3'):

    #build a new table named by the journal title 

    sql_new = "create table rec_email3 (id int not null unique auto_increment, author varchar(100) Null,"

    sql_new+="email varchar(100) Null,"

    sql_new+="response int Null,"

    sql_new+="confidence int Null,"

    sql_new+="cn varchar(100) Null,"

    sql_new+="country varchar(100) Null,"

    sql_new+="journal varchar(100) Null,"

    sql_new+="citation varchar(100) Null,"

    sql_new+="volume varchar(100) Null,"

    sql_new+="year varchar(100) Null,"

    sql_new+="title varchar(1000) Null,"

    sql_new+="attempt varchar(1000) Null,"

    sql_new+="primary key(id))"

    cur.execute(sql_new)

    conn.commit()


#建立新表all_inf
#建立完整的新表
if not table_exist('all_inf1'):

    #build a new table named by the journal title 

    sql_new = "create table all_inf1(id int not null unique auto_increment, author varchar(100) Null,"

    sql_new+="email varchar(100) Null,"

    sql_new+="response int Null,"

    sql_new+="confidence int Null,"

    sql_new+="cn varchar(100) Null,"

    sql_new+="country varchar(100) Null,"

    sql_new+="journal varchar(100) Null,"

    sql_new+="citation varchar(100) Null,"

    sql_new+="volume varchar(100) Null,"

    sql_new+="year varchar(100) Null,"

    sql_new+="title varchar(1000) Null,"

    sql_new+="attempt varchar(1000) Null,"
    
    sql_new+="sendstate int Null,"
    
    sql_new+="primary key(id))"

    cur.execute(sql_new)

    conn.commit()

#将rec和author表添加到总表中
#==============================================================================
# sql_select = "select * from rec_email3"
# 
# cur.execute(sql_select)
# 
# info = cur.fetchall()
# 
# for i in range(0,len(info)):
# 
#         #将该作者信息添加总表格中
# 
#         # update the table  all_inf
# 
#     sql_add = "insert into all_inf1(id,author,email,response,confidence, cn, country, journal, citation, volume, year, title, sendstate,attempt)values("
# 
#     sql_add+= "\"%d\","%(i+1)
#     
#     sql_add+="\"%s\","%info[i][1].split('\'')[0]  # author name
# 
#     sql_add+="\"%s\","%info[i][2].split('\'')[0]  # email address
# 
#     sql_add+="\"1\","  # Num of attempts
# 
#     sql_add+="\"%s\","%info[i][4] #confidence
# 
#     sql_add+="\"%s\","%info[i][5].split('\'')[0]   #  cn
# 
#     sql_add+="\"%s\","%info[i][6].split('\'')[0]   # country
# 
#     sql_add+="\"%s\","%info[i][7].split('\'')[0]   #  journal   
# 
#     sql_add+="\"%s\","%info[i][8].split('\'')[0]   #  citation
# 
#     sql_add+="\"%s\","%info[i][9].split('\'')[0]   #  volume
# 
#     sql_add+="\"%s\","%info[i][10].split('\'')[0]  #  year
# 
#     sql_add+="\"%s\","%info[i][11].split('\'')[0]  #  title
# 
#     sql_add+="\"1\","# 已发送成功则state为1
#     
#     sql_add+='"%s")'%info[i][12].split('\'')[0]#attempt time
# 
#     cur.execute(sql_add)
# 
#     conn.commit()
# 
# 
# sql_select = "select * from email_jour_auth3"
# 
# cur.execute(sql_select)
# 
# num = len(info)+1
# 
# info = cur.fetchall()
# 
# for i in range(506,len(info)):
#    
#    
#     now_name = info[i][1].split('\'')[0]
# 
# 
#     sql_find = 'select * from rec_email3 where author=\"%s\"'%now_name
# 
#     cur.execute(sql_find)
# 
#     cnt = cur.fetchall()
# 
#     if(len(cnt)==0):     #若未出现在总表中
# 
#         #将该作者信息添加总表格中
# 
#         # update the table  all_inf
# 
#             sql_add = "insert into all_inf1(id,author,email,response,confidence, cn, country, journal, citation, volume, year, title, sendstate)values("
# 
#             sql_add+= "\"%d\","%(num)
#             
#             num = num +1
#             
#             sql_add+="\"%s\","%info[i][1].split('\'')[0]  # author name
# 
#             sql_add+="\"%s\","%info[i][2].split('\'')[1]  # email address
# 
#             sql_add+="\"1\","  # Num of attempts
# 
#             sql_add+="\"%s\","%info[i][4] #confidence
# 
#             sql_add+="\"%s\","%info[i][5].split('\'')[1]   #  cn
# 
#             sql_add+="\"%s\","%info[i][6].split('\'')[1]   # country
# 
#             sql_add+="\"%s\","%info[i][7].split('\'')[1]   #  journal   
# 
#             sql_add+="\"%s\","%info[i][8].split('\'')[1]   #  citation
# 
#             sql_add+="\"%s\","%info[i][9].split('\'')[1]   #  volume
# 
#             sql_add+="\"%s\","%info[i][10].split('\'')[1]  #  year
# 
#             sql_add+="\"%s\","%info[i][11].split('\'')[1]  #  title
# 
#             sql_add+="\"0\")"# 未尝试过state为0
# 
#             cur.execute(sql_add)
# 
#             conn.commit()
# 
#==============================================================================




#从all_inf中选择sendstate为0的作者发送邮件
sql_select = "select * from all_inf1 where sendstate=\"0\""

cur.execute(sql_select)

info = cur.fetchall()

suc = 0

fails = 0

for i in range(0,len(info)): 

    modifiedcontent = mailcontent.split('XXX')[0] + info[i][11].split('\'')[1] + mailcontent.split('XXX')[1]

    content = 'Dear Dr. ' + info[i][1].split('\'')[1]+'\n' + modifiedcontent                         #发送1封，上面的列表是几个人，这个就填几  

    

    # Check if the author has been in touched (No. 2)

    now_name = info[i][1].split('\'')[1]

    if send_mail(info[i][2].split('\'')[1],mailsub,content):
        print("Mail sent to "+info[i][2].split('\'')[1]+' successfully!')
        suc = suc + 1
    # 若发送成功，修改sendstate为1，并记录发送成功时间
        sql_update = "update all_inf1 set sendstate = '1', attempt = \"%s\""%time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        sql_update += " where author = '%s'"%now_name

        cur.execute(sql_update)

        conn.commit()

    else:  

        print("failed to be received by "+info[i][2].split('\'')[1]+'!')

        fails = fails + 1

        flog.writelines('failed to be received by '+info[i][2].split('\'')[1]+'!' + '\n')



flog.writelines('In total, there is '+ str(suc) + ' messages has been sent successfully while ' +str(fails)+ ' messages can not be sent. \n')

flog.writelines('End at: '+ time.strftime('%H:%M:%S',time.localtime(time.time())) + '\n')

#send_mail('ibs@zjgsu.edu.cn','Mail Log', flog.read())   

flog.close()   


        
