# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 22:22:10 2018

@author: Ni He
"""

# fuzzywuzzy import fuzz
from fuzzywuzzy import process
# pip install fuzzywuzzy
# pip install fuzzywuzzy[speedup]
import mysql.connector
from pypinyin import lazy_pinyin

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
        cname = '0'
    return cname
        

conn = mysql.connector.connect(host="localhost",port=3306,user="root",\
                       password= '11031103',database="journal_list",charset="utf8")
cur = conn.cursor()

sql_create = 'create table email_jour_auth (id int unsigned auto_increment primary key, \
    author varchar(50) null, email varchar(50) null, \
    confidence int(20) null, cn varchar(20) null, country varchar(20) null,\
    journal varchar(50) null, citation varchar(20) null, \
    title varchar(200) null, url varchar(200) null)'
cur.execute(sql_create)

nam_jour = 'aos'
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
        
        sql_ins = 'insert into email_jour_auth (author, email, confidence, cn, country, journal, citation, title, url) \
        values ("%s","%s","%s","%s","%s","%s","%s","%s","%s")'
        cont_ins = [au_email[0],em,au_email[1], cname ,country,nam_jour,citations[i][0], titles[i][0], urls[i][0]]
        cur.execute(sql_ins, cont_ins)
    conn.commit()
    

