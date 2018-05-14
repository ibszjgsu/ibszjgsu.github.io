# -*- coding: utf-8 -*-
"""
@author Ni He
"""

import itchat, random
import time


def find_friend(RemarkName):
  for friend in itchat.get_friends():
    if friend['RemarkName'] == RemarkName:
      return friend


itchat.auto_login(True)
friendID = find_friend('叶珍珍')
wish = [u'去你的',u'滚',u'想死呀',u'考试挂科咯!']

no = 0

while no < 20: # 骚扰20次
    no = no + 1
    #if time.time() - start_time > 10: #  每30秒发一次，可以改时间间隔
        #start_time = time.time()
    a_wish=random.choice(wish)
    itchat.send_msg(a_wish,toUserName=friendID['UserName'])
    time.sleep(10) # 暂停10秒





