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


headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) \
           AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
          }

pageurl = 'G:\\Git\\science_direct_eng.html'

soup = BeautifulSoup(open(pageurl), 'html.parser', from_encoding="utf-8")
sp = soup.find_all(href=re.compile("https://www.sciencedirect.com/science/journal/"))

info =[]
for link in sp:
    info.append([link.text.replace('&','and').replace('.','').replace(',','').replace(':','').replace('-','').replace('  ',' ').replace(' ','_'),link.get('href')])

csv_columns = ['journal_name', 'journal_url']

currentPath = os.getcwd()
csv_file = currentPath + "\\csv\\ScienceDirect_eng.csv"

WriteListToCSV(csv_file,csv_columns,info)