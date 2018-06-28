# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 22:08:18 2018

@author: Administrator
"""

import csv
import mysql.connector

#连接MySQL数据库
conn = mysql.connector.connect(host="10.23.0.2",port=3306,user="root",\
                       password="11031103",database="journalcontact",charset="utf8")
cur = conn.cursor()

sql = "create table ScienceDirect_human (id int not null unique auto_increment, \
         name varchar(200), journal_id varchar(200),\
         primary key(id))"
cur.execute(sql)

with open('ScienceDirect_humanity4.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        sql = "insert into ScienceDirect_human (name, journal_id) \
        values ('%s', '%s')" % (row[0], row[1])
        cur.execute(sql)
        print(row)