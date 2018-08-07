# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 16:55:49 2018

@author: Ni He
"""

from selenium import webdriver            
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.options import Options 
import time, re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

class DataSaver(object):
    
    def __init__(self):
        self.host = "10.23.0.2"
        self.port = 3306
        self.user = "root"
        self.pw = "11031103"
        self.charset = "utf8"
        self.sql_eng = 'mysql+mysqldb://root:11031103@10.23.0.2:3306/cnki?charset=utf8'
        
    def save_into_database_engine(self, table_to_save, table_name):
        engine = create_engine(self.sql_eng) 
        try:
            pd.io.sql.to_sql(table_to_save, table_name, engine, schema = 'cnki', if_exists = 'append', index = False)
        except:
            print('Error in MySQL')
        finally:
            engine.dispose()
    
    def database_execute_engine(self, sql_exec):
        engine = create_engine(self.sql_eng) 
        engine.execute(sql_exec)
        engine.dispose()

    def download_chrome_driver(self, url, sleep = 'y'):
        chrome_options = Options()
            #prefs = {"profile.managed_default_content_settings.images": 2}
            #chrome_options.add_experimental_option("prefs", prefs)
            #chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('-headless')
        chrome_options.add_argument('-disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        if sleep == 'y':
            time.sleep(np.random.randint(1,10,1))
        #self.driver = driver
        return driver


def get_journal_list():
    url = 'http://navi.cnki.net/knavi/Journal.html'
    ds = DataSaver()
    driver = ds.download_chrome_driver(url)
    # create table 
    sql = 'create table journal_list(id int auto_increment,\
           title varchar(800), url varchar(250), multi_factor varchar(100), comp_factor varchar(100),\
           PRIMARY KEY(id))' 
            #engine.execute(sql)
    ds.database_execute_engine(sql)
    # 点击学术期刊
    driver.find_element_by_xpath('//*[@id="rightnavi"]/ul/li[2]/a').click()
    # 选择核心期刊
    driver.find_element_by_xpath('//*[@id="rightnavi"]/div/div[1]/div/div[1]/a').click()
    # start to collect, 94 pages in total
    p = 94
    while p > 0:
        p = p - 1
        content = driver.page_source.encode('utf-8')
        time.sleep(np.random.randint(1,10,1))
        soup = BeautifulSoup(content, 'lxml')
        urls = soup.find_all(class_='list_tup')[0].find_all('a')
        # collect in each page
        journal_list = pd.DataFrame(columns=['title', 'url','multi_factor','comp_factor'])
        tmp = {}
        for u in urls:
            tmp['title'] = u.get('title')  # name of journal
            tmp['url'] = 'http://navi.cnki.net' + u.get('href').split(' ')[-1]  # url
            tmp['multi_factor'] = u.find_all('p')[0].text.split('：')[-1]
            tmp['comp_factor'] = u.find_all('p')[1].text.split('：')[-1]
            journal_list = journal_list.append(tmp, ignore_index=True)
        
        if len(journal_list) > 0:
            ds.save_into_database_engine(journal_list, 'journal_list')
            print('%d journals have been saved at %s' % (len(journal_list), time.strftime('%Y-%m-%d at %H:%M:%S',time.localtime(time.time()))))            
        # click next page
        driver.find_element_by_xpath('//*[@id="rightnavi"]/div/div[3]/a[13]').click()
        
