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


def find_surname(name):
    ChineseSurname = '赵 钱 孙 李 周 吴 郑 王 冯 陈 褚 卫 蒋 沈 韩 杨 朱 秦 尤 许 何 吕 施 张 孔 曹 严 华 金 魏 陶 姜 戚 谢 邹 喻 柏 水 窦 章 云 苏 潘 葛 奚 范 彭 郎 鲁 韦 昌 马 苗 凤 花 方 俞 任 袁 柳 酆 鲍 史 唐 费 廉 岑 薛 雷 贺 倪 汤 滕 殷 罗 毕 郝 邬 安 常 乐 于 时 傅 皮 卞 齐 康 伍 余 元 卜 顾 孟 平 黄 和 穆 萧 尹 姚 邵 湛 汪 祁 毛 禹 狄 米 贝 明 臧 计 伏 成 戴 谈 宋 茅 庞 熊 纪 舒 屈 项 祝 董 梁 杜 阮 蓝 闵 席 季 麻 强 贾 路 娄 危 江 童 颜 郭 梅 盛 林 刁 锺 徐 邱 骆 高 夏 蔡 田 樊 胡 凌 霍 虞 万 支 柯 昝 管 卢 莫 经 房 裘 缪 干 解 应 宗 丁 宣 贲 邓 郁 单 杭 洪 包 诸 左 石 崔 吉 钮 龚 程 嵇 邢 滑 裴 陆 荣 翁 荀 羊 於 惠 甄 麴 家 封 芮 羿 储 靳 汲 邴 糜 松 井 段 富 巫 乌 焦 巴 弓 牧 隗 山 谷 车 侯 宓 蓬 全 郗 班 仰 秋 仲 伊 宫 宁 仇 栾 暴 甘 钭 历 戎 祖 武 符 刘 景 詹 束 龙 叶 幸 司 韶 郜 黎 蓟 溥 印 宿 白 怀 蒲 邰 从 鄂 索 咸 籍 赖 卓 蔺 屠 蒙 池 乔 阳 郁 胥 能 苍 双 闻 莘 党 翟 谭 贡 劳 逄 姬 申 扶 堵 冉 宰 郦 雍 却 璩 桑 桂 濮 牛 寿 通 边 扈 燕 冀 僪 浦 尚 农 温 别 庄 晏 柴 瞿 阎 充 慕 连 茹 习 宦 艾 鱼 容 向 古 易 慎 戈 廖 庾 终 暨 居 衡 步 都 耿 满 弘 匡 国 文 寇 广 禄 阙 东 欧 殳 沃 利 蔚 越 夔 隆 师 巩 厍 聂 晁 勾 敖 融 冷 訾 辛 阚 那 简 饶 空 曾 毋 沙 乜 养 鞠 须 丰 巢 关 蒯 相 查 后 荆 红 游 竺 权 逮 盍 益 桓 公 丛 岳'
    surnames = ChineseSurname.split(' ')
    pinyinsur = lazy_pinyin(surnames)
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
 
# 邮件发送单元
def send_mail(to_list,sub,content,mail_pass):  
    mail_host="mail.zjgsu.edu.cn"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址  
    mail_user="recruit.ibs"                           #用户名  
    mail_postfix="zjgsu.edu.cn"                     #邮箱的后缀，网易就是163.com
    
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

 

# 连接数据库
conn = mysql.connector.connect(host="10.23.0.2",port=3306,user="root",\
                       password= '11031103',database="journalcontact",charset="utf8")
cur = conn.cursor()


    
if not table_exist('all_info'):
    #build a new table named by the journal title 
    sql_new = "create table all_info (id int not null unique auto_increment, author varchar(100) Null,"
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
sql = "select * from "+ nam_jour
cur.execute(sql)
# id, title, author_list, email_list, citation, vol, issue, year, URL
new_author_info = cur.fetchall()


# 根据文章数进行循环，每篇文章会有大于等于一个作者
for i in range(len(new_author_info)):
    # If there is no emailaddress then skip this record
    if new_author_info[i][3] == '[]':
        continue 
    # Convert the string to a list, even for one item sting
    emails = new_author_info[i][3].split(',')
    author = new_author_info[i][2].split(';')
    
    for email in emails:
        # 智能识别邮件用户名和作者姓名之间的关系 返回 au_email[0]是邮件地址 au_email[0]是置信度 
        (au_email,) = process.extract(email.split('@')[0], author, limit=1)
        # 识别国别
        if email.split('@')[1].split('.')[-1] == 'edu':
            country = 'US'
        else:
            country = str.upper(email.split('@')[1].split('.')[-1])
        # 安置相应的中文名字，多音字无法处理    
        cname = find_surname(str.lower(au_email[0].split(',')[0].split(' ')[-1]))        
        # 对于能够识别成相应中文名字以及识别置信度高于50的，进行数据库记录
        if not cname == 'NULL' and au_email[1] > 10:
            # 一个author只有可以使用一次，被email地址匹配过的author name 就从list中去掉
            author = [au for au in author if au not in list(au_email)]

            # 寻找是否已经输入该作者信息，包括姓名和邮箱地址，如果同一作者出现第二个邮箱也认为是第二条记录 
            sql_find = 'select * from all_info where email= %s'
            cont_find = [email]
            cur.execute(sql_find,cont_find)
            cnt = cur.fetchall()
            # 判断是否有重复，没有则插入
            if(len(cnt)==0):   
                sql_ins = 'insert into all_info (author, email, confidence, cn, country, journal, citation, volume, year, title, sendstate) \
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                cont_ins = [au_email[0].strip(), email, au_email[1], cname ,country,nam_jour,new_author_info[i][4],new_author_info[i][5], new_author_info[i][7], new_author_info[i][1], 0]
                cur.execute(sql_ins, cont_ins)
                conn.commit()
 


## 以下部分是邮件发送部分，可以单独使用和上面代码独立

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
    
#从all_inf1中筛选sendstate为0的作者发送邮件，并将发送成功的人状态改成1 
sql_select = "select * from all_info where sendstate = 0"
cur.execute(sql_select)
info = cur.fetchall()
# 计数器
suc = 0
fails = 0
mail_pass=input('Please enter the password of the sending mailbox:')     #密码  
for i in range(len(info)): 
    modifiedcontent = mailcontent.split('XXX')[0] + info[i][11] + mailcontent.split('XXX')[1]
    content = 'Dear Dr. ' + info[i][1] + modifiedcontent                         #发送1封，上面的列表是几个人，这个就填几     
    # Check if the author has been in touched (No. 2)
    now_name = info[i][1]
    if send_mail(info[i][2],mailsub,content,mail_pass):
        print("Mail sent to "+info[i][2]+' successfully!')
        suc = suc + 1
    # 若发送成功，修改sendstate为1，并记录发送成功时间
        sql_update = "update all_info set sendstate = %s, attempt = %s where author = %s"
        cont_ins = [1, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), now_name]
        cur.execute(sql_update, cont_ins)
        conn.commit()

    else:  
        print("failed to be received by "+info[i][2]+'!')
        fails = fails + 1
        flog.writelines('failed to be received by '+info[i][2]+'!' + '\n')



flog.writelines('In total, there is '+ str(suc) + ' messages has been sent successfully while ' +str(fails)+ ' messages can not be sent. \n')
flog.writelines('End at: '+ time.strftime('%H:%M:%S',time.localtime(time.time())) + '\n')
flog.close()   
    
