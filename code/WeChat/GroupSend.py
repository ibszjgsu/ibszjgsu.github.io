# -*- coding: utf-8 -*-
"""
Created on Sun May  6 15:44:17 2018

@author: Ni He
"""

import itchat
#import pandas as pd
import os, sys

def find_friend(nick_name):
  for friend in itchat.get_friends():
    if friend['RemarkName'] == nick_name:
      return friend

#def main():
#  itchat.auto_login(True)
#  friends = itchat.get_friends(update = True)
#  roomslist = itchat.get_chatrooms()
#  aea = itchat.search_friends(name = 'aea')
#  friend = find_friend(u'spiritual')
#  username = friend['UserName']
#  itchat.send(msg=u'你好啊',toUserName=username)
#  itchat.logout()
#
#if __name__ == "__main__":
#  main()
fileloc = os.getcwd()
#namelist = pd.read_csv(fileloc + '\\namelist.csv')
  
itchat.auto_login(True)
friendlist = ['陈晶晶','颜莎莎','王伟波']
solutionlist = ['陈女士','颜女士','王先生']
for i in range(0,len(friendlist)):
    content = solutionlist[i] + u'您好呀, 这个是机器发送的，不要回复我 \n 再见'
    friend = find_friend(friendlist[i])
    username = friend['UserName']
    itchat.send(msg=content,toUserName=username)
    img = fileloc + '\\logo.gif'
    itchat.send_image(img,toUserName=username)
#
#　发送文件： msg='@fil@path_to_file'
#
#　　发送图片：msg='@img@path_to_img'
#
#　　发送视频：msg='@vid@path_to_vid'