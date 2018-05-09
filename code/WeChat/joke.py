# -*- coding: utf-8 -*-
"""
Created on Sun May  6 15:44:17 2018

@author: Ni He
"""

import itchat, random
#import pandas as pd


def find_friend(nick_name):
  for friend in itchat.get_friends():
    if friend['RemarkName'] == nick_name:
      return friend


itchat.auto_login(True)
friendID = find_friend('小老虎')
SINCERE_WISH = [u'去你的',u'滚',u'想死呀',u'见鬼吧~',u'考试挂科咯!']
#SINCERE_WISH = [u'祝中秋快乐',u'中秋快乐呀',u'中秋快乐哟',u'中秋节快乐呀~',u'中秋节快乐!',u'中秋国庆快乐!']

@itchat.msg_register(itchat.content.TEXT)   #这里的TEXT表示如果有人发送文本消息，那么就会调用下面的方法
def simple_reply(msg, friendID):
    #这个是向发送者发送消息
    for i in range(0,10):  
        SEND_WISH=random.choice(SINCERE_WISH)
        if msg['FromUserName'] == friendID['UserName']:
            itchat.send_msg(SEND_WISH,toUserName=friendID['UserName'])
    return     



