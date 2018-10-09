# -*- coding: utf-8 -*-
"""
Created on Sun May  6 15:44:17 2018

@author: Ni He
"""

import itchat
#import pandas as pd
import os, sys
import csv


#
#　发送文件： msg='@fil@path_to_file'

#
#　　发送视频：msg='@vid@path_to_vid'

sentinfo = open('namelist.csv','r', encoding='utf-8-sig')
reader = csv.reader(sentinfo)
data = []
for item in reader:
    data.append(item)
sentinfo.close()



itchat.auto_login(True)
for info in data[1:]:
    content = u'尊敬的' + info[1] + u'， 您好，祝您中秋节快乐。 倪禾'
    username = itchat.search_friends(name=info[0])[0].UserName
    itchat.send(msg=content,toUserName=username)

friendlist = data[1:]
solutionlist = ['波哥']

for i in range(0,len(friendlist)):
    content = solutionlist[i] + u'您好呀, 这个是机器发送的，不要回复我 \n 再见'
    username = itchat.search_friends(name=friendlist[i])[0].UserName
    itchat.send(msg=content,toUserName=username)


