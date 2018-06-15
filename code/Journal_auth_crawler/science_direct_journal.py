# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 21:22:21 2018

@author: Administrator
"""

import requests
#from lxml import etree
import re
import mysql.connector
import time
from bs4 import BeautifulSoup
import os
import csv

def WriteListToCSV(csv_file,csv_columns,data_list):
    try:
        with open(csv_file, 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(csv_columns)
            for data in data_list:
                writer.writerow(data)
    except:
            print("I/O error")    
    return 

def table_exist(tab_name):
    cur.execute('show tables')  # 罗列所有当前库里面的所有表格
    tables = cur.fetchall()
    selectab = re.compile(r'\w*\w*')
    tabnames = selectab.findall(str(tables))
    res = tab_name in tabnames
    return res

headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) \
           AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
          }

#连接MySQL数据库
conn = mysql.connector.connect(host="10.23.0.2",port=3306,user="root",\
                       password="11031103",database="science_direct",charset="utf8")
cur = conn.cursor()



journal_url = 'https://www.sciencedirect.com/science/journal/00014575'

res = requests.get(journal_url, timeout = 30, headers=headers)
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'html.parser')

pat = soup.find_all(href=re.compile('/issues'))
if len(pat) > 1:
    jou_all_issue_url = 'https://www.sciencedirect.com' + pat[0].get('href')
else:
    jou_all_issue_url = 'https://www.sciencedirect.com' + pat.get('href')
    
res_issue = requests.get(jou_all_issue_url, timeout = 30, headers = headers)
res_issue.encoding = 'utf-8'
soup = BeautifulSoup(res_issue.text, 'html.parser')

pat = soup.find_all(class_='anchor text-m')




soup = BeautifulSoup(open(pageurl), 'html.parser', from_encoding="utf-8")
sp = soup.find_all(href=re.compile("https://www.sciencedirect.com/science/journal/"))

info =[]
for link in sp:
    info.append([link.text.replace('&','and').replace('.','').replace(',','').replace(':','').replace('-','').replace('  ',' ').replace(' ','_'),link.get('href')])

csv_columns = ['journal_name', 'journal_url']

currentPath = os.getcwd()
csv_file = currentPath + "\\csv\\ScienceDirect_humanity4.csv"

WriteListToCSV(csv_file,csv_columns,info)