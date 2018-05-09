# -*- coding: utf-8 -*-
"""
Created on Tue May  8 01:11:41 2018

@author: Administrator
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

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    if msg['ToUserName'] != friendID['UserName']: return
    SEND_WISH=random.choice(SINCERE_WISH)
    itchat.send_msg(SEND_WISH,toUserName=friendID['UserName'])
    return

itchat.auto_login(hotReload=True)
itchat.run()