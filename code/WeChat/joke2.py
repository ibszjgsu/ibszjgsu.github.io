# -*- coding: utf-8 -*-
"""
Created on Tue May  8 01:11:41 2018

@author: Administrator
"""

import itchat

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    return msg['Text']

itchat.auto_login(hotReload=True)
itchat.run()