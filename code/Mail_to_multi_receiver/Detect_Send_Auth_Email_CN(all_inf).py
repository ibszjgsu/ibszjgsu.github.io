 # -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 22:22:10 2018

@author: Ni He
"""

"""
需要修改的地方就是期刊的名称（ejos 一处），其他地方无需修改
"""

# fuzzywuzzy import fuzz
from fuzzywuzzy import process
# pip install fuzzywuzzy
# pip install fuzzywuzzy[speedup]
import mysql.connector
from pypinyin import lazy_pinyin
import re
import smtplib  
from email.mime.text import MIMEText  
import os
import time


global surnames, pinyinsur
ChineseSurname = '赵 钱 孙 李 周 吴 郑 王 冯 陈 褚 卫 \
蒋 沈 韩 杨 朱 秦 尤 许 何 吕 施 张 \
孔 曹 严 华 金 魏 陶 姜 戚 谢 邹 喻 \
柏 水 窦 章 云 苏 潘 葛 奚 范 彭 郎 \
鲁 韦 昌 马 苗 凤 花 方 俞 任 袁 柳 \
酆 鲍 史 唐 费 廉 岑 薛 雷 贺 倪 汤 \
滕 殷 罗 毕 郝 邬 安 常 乐 于 时 傅 \
皮 卞 齐 康 伍 余 元 卜 顾 孟 平 黄 \
和 穆 萧 尹 姚 邵 湛 汪 祁 毛 禹 狄 \
米 贝 明 臧 计 伏 成 戴 谈 宋 茅 庞 \
熊 纪 舒 屈 项 祝 董 梁 杜 阮 蓝 闵 \
席 季 麻 强 贾 路 娄 危 江 童 颜 郭 \
梅 盛 林 刁 锺 徐 邱 骆 高 夏 蔡 田 \
樊 胡 凌 霍 虞 万 支 柯 昝 管 卢 莫 \
经 房 裘 缪 干 解 应 宗 丁 宣 贲 邓 \
郁 单 杭 洪 包 诸 左 石 崔 吉 钮 龚 \
程 嵇 邢 滑 裴 陆 荣 翁 荀 羊 於 惠 \
甄 麴 家 封 芮 羿 储 靳 汲 邴 糜 松 \
井 段 富 巫 乌 焦 巴 弓 牧 隗 山 谷 \
车 侯 宓 蓬 全 郗 班 仰 秋 仲 伊 宫 \
宁 仇 栾 暴 甘 钭 历 戎 祖 武 符 刘 \
景 詹 束 龙 叶 幸 司 韶 郜 黎 蓟 溥 \
印 宿 白 怀 蒲 邰 从 鄂 索 咸 籍 赖 \
卓 蔺 屠 蒙 池 乔 阳 郁 胥 能 苍 双 \
闻 莘 党 翟 谭 贡 劳 逄 姬 申 扶 堵 \
冉 宰 郦 雍 却 璩 桑 桂 濮 牛 寿 通 \
边 扈 燕 冀 僪 浦 尚 农 温 别 庄 晏 \
柴 瞿 阎 充 慕 连 茹 习 宦 艾 鱼 容 \
向 古 易 慎 戈 廖 庾 终 暨 居 衡 步 \
都 耿 满 弘 匡 国 文 寇 广 禄 阙 东 \
欧 殳 沃 利 蔚 越 夔 隆 师 巩 厍 聂 \
晁 勾 敖 融 冷 訾 辛 阚 那 简 饶 空 \
曾 毋 沙 乜 养 鞠 须 丰 巢 关 蒯 相 \
查 后 荆 红 游 竺 权 逮 盍 益 桓 公 \
丛 岳'
surnames = ChineseSurname.split(' ')
pinyinsur = lazy_pinyin(surnames)
    
def findsurname(name):
    if name in pinyinsur:
        cname = surnames[pinyinsur.index(name)]
    else:
        cname = 'NULL'
    return cname
        

def table_exist(tab_name):
    cur.execute('show tables')  # 罗列所有当前库里面的所有表格
    tables = cur.fetchall()
    selectab = re.compile(r'\w*\w*')
    tabnames = selectab.findall(str(tables))
    res = tab_name in tabnames
    return res


 

mail_host="mail.zjgsu.edu.cn"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址  
mail_user="recruit.ibs"                           #用户名  
mail_pass=input('Please enter the password of the sending mailbox:')     #密码  
mail_postfix="zjgsu.edu.cn"                     #邮箱的后缀，网易就是163.com

 

def send_mail(to_list,sub,content):  

    me="International Business School in Zhejiang Gongshang Univ "+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = to_list                #将收件人列表以‘；’分隔  

    try:  
        time.sleep(3)#睡眠2秒 
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

# Log

flog = open(os.getcwd() + '\\log.txt', 'a+')  # 读取日志内容

flog.writelines('\n \n Date Updating Log on ' + time.strftime('%Y-%m-%d',time.localtime(time.time())) + '\n')

flog.writelines('Start from: '+ time.strftime('%H:%M:%S',time.localtime(time.time())) + '\n')




conn = mysql.connector.connect(host="10.23.0.2",port=3306,user="root",\
                       password= '11031103',database="journalcontact",charset="utf8")
cur = conn.cursor()

if not table_exist('email_jour_auth3'):
    sql_create = 'create table email_jour_auth3 (id int unsigned auto_increment primary key, \
        author varchar(50) null, email varchar(50) null, sent int(5) null, \
        confidence int(20) null, cn varchar(20) null, country varchar(20) null,\
        journal varchar(50) null, citation varchar(20) null, volume varchar(20) null, year varchar(20) null,\
        title varchar(200) null, url varchar(200) null)'
    cur.execute(sql_create)
    
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


nam_jour = 'ss'
sql = "select authors from "+ nam_jour
cur.execute(sql)
author_list = cur.fetchall()
sql = "select au_email from "+ nam_jour
cur.execute(sql)
email_list = cur.fetchall()
sql = "select title from "+ nam_jour
cur.execute(sql)
titles = cur.fetchall()
sql = "select citation from "+ nam_jour
cur.execute(sql)
citations = cur.fetchall()
sql = "select url from "+ nam_jour
cur.execute(sql)
urls = cur.fetchall()
sql = "select volume from "+ nam_jour
cur.execute(sql)
vols = cur.fetchall()
sql = "select year from "+ nam_jour
cur.execute(sql)
yrs = cur.fetchall()

suc = 0
fails = 0
for i in range(1,len(titles)):
    (emails,) = email_list[i]
    (authors,) = author_list[i]
    # If there is no emailaddress then skip this record
    if emails == '[]':
        continue 
    # Convert the string to a list, even for one item sting
    email = emails.split(',')
    author = authors.split(';')
    for em in email:
        (au_email,) = process.extract(em.split('@')[0], author, limit=1)
        if em.split('@')[1].split('.')[-1] == 'edu':
            country = 'US'
        else:
            country = str.upper(em.split('@')[1].split('.')[-1])
            
        cname = findsurname(str.lower(au_email[0].split(',')[0].split(' ')[-1]))
        
        
        if not cname == 'NULL' and au_email[1] > 50:

            sql_ins = 'insert into email_jour_auth3 (author, email, sent, confidence, cn, country, journal, citation, volume, year, title, url) \
            values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'

            cont_ins = [au_email[0],em, 0, au_email[1], cname ,country,nam_jour,citations[i][0],vols[i][0], yrs[i][0], titles[i][0], urls[i][0]]

            cur.execute(sql_ins, cont_ins)
             
            sql_find = 'select * from all_inf1 where author=\"%s\" and email=\"%s\"'
            cont_ins=[au_email[0],em]
            cur.execute(sql_find,cont_ins)
            cnt = cur.fetchall()
 
            if(len(cnt)==0):   
                sql_ins = 'insert into all_inf1 (author, email, confidence, cn, country, journal, citation, volume, year, title, sendstate) \
                values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'

                cont_ins = [au_email[0],em,  au_email[1], cname ,country,nam_jour,citations[i][0],vols[i][0], yrs[i][0], titles[i][0], 0]
                cur.execute(sql_ins, cont_ins)
    conn.commit()
  
    
#从all_inf1中筛选sendstate为0的作者发送邮件
sql_select = "select * from all_inf1 where sendstate=\"0\""

cur.execute(sql_select)

info = cur.fetchall()

suc = 0

fails = 0

for i in range(0,len(info)): 

    modifiedcontent = mailcontent.split('XXX')[0] + info[i][11] + mailcontent.split('XXX')[1]

    content = 'Dear Dr. ' + info[i][1] + modifiedcontent                         #发送1封，上面的列表是几个人，这个就填几  

    

    # Check if the author has been in touched (No. 2)

    now_name = info[i][1]

    if send_mail(info[i][2],mailsub,content):
        print("Mail sent to "+info[i][2]+' successfully!')
        suc = suc + 1
    # 若发送成功，修改sendstate为1，并记录发送成功时间
        sql_update = "update all_inf1 set sendstate = '1', attempt = \"%s\""%time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        sql_update += " where author = '%s'"%now_name

        cur.execute(sql_update)

        conn.commit()

    else:  

        print("failed to be received by "+info[i][2]+'!')

        fails = fails + 1

        flog.writelines('failed to be received by '+info[i][2]+'!' + '\n')



flog.writelines('In total, there is '+ str(suc) + ' messages has been sent successfully while ' +str(fails)+ ' messages can not be sent. \n')

flog.writelines('End at: '+ time.strftime('%H:%M:%S',time.localtime(time.time())) + '\n')

#send_mail('ibs@zjgsu.edu.cn','Mail Log', flog.read())   

flog.close()   
    
