# -*- coding: utf-8 -*-
"""
Created on Sat May 12 14:54:03 2018

@author: Ni He
"""

#-*- encoding: utf-8 -*-
import sys
import locale
import poplib
from email import parser
import email
import string
# 确定运行环境的encoding
__g_codeset = sys.getdefaultencoding()
if "ascii"==__g_codeset:
  __g_codeset = locale.getdefaultlocale()[1]
#
def object2double(obj):
  if(obj==None or obj==""):
    return 0
  else:
    return float(obj)
  #end if
#
def utf8_to_mbs(s):
  return s.decode("utf-8").encode(__g_codeset)
#
def mbs_to_utf8(s):
  return s.decode(__g_codeset).encode("utf-8")
#
host = 'mail.zjgsu.edu.cn'
username = 'recruit.ibs'
password = '$Ibs11031103'
pop_conn = poplib.POP3_SSL(host)
pop_conn.user(username)
pop_conn.pass_(password)
#Get messages from server:
# 获得邮件
messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
#print messages
#print "--------------------------------------------------"
# Concat message pieces:
messages = ["\n".join(mssg[1]) for mssg in messages]
#print messages
#Parse message intom an email object:
# 分析
messages = [parser.Parser().parsestr(mssg) for mssg in messages]
i = 0