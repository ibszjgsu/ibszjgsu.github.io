# -*- coding: utf-8 -*-
"""
Created on Tue May  8 01:32:05 2018

@author: Administrator
"""

import os
import itchat
# 通过该命令安装该API： pip install NetEaseMusicApi
from NetEaseMusicApi import interact_select_song

with open('stop.mp3', 'w') as f: pass
def close_music():
    os.startfile('stop.mp3')
    


@itchat.msg_register(itchat.content.TEXT)
def music_player(msg):
    if msg['ToUserName'] != 'filehelper': return
    if msg['Text'] == u'关闭':
        close_music()
        itchat.send(u'音乐已关闭', 'filehelper')
    if msg['Text'] == u'帮助':
        itchat.send(u'帮助信息', 'filehelper')
    else:
        itchat.send(interact_select_song(msg['Text']), 'filehelper')

itchat.auto_login(True)
itchat.send(HELP_MSG, 'filehelper') 
itchat.run()