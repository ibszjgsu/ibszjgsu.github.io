# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 17:00:32 2018

@author: Administrator
"""

#  http://npm.taobao.org/mirrors/chromedriver/   chromedriver 镜像下载

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from sqlalchemy import create_engine
import pandas as pd
#import pymysql
#pymysql.install_as_MySQLdb()

engine = create_engine('mysql+mysqldb://root:11031103@localhost:3306/science_direct?charset=utf8') 
#pd.io.sql.to_sql(journal_issue_list, 'journal_issue_list', engine, schema='science_direct', if_exists='replace') 
#ret = pd.read_sql_query("select id, iss_url from journal_issue_list", engine)

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

#driver = webdriver.Chrome(executable_path='C:/ProgramData/Anaconda3/selenium/webdriver/chromedriver/chromedriver.exe', chrome_options=chrome_options)
driver = webdriver.Chrome(chrome_options=chrome_options)

print('start testing...')
time_start = time.time()
driver.get('https://www.sciencedirect.com/')
print(driver.title)

print('Closing')
driver.close()
print('It takes %s seconds.' % (time.time()-time_start))