# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 14:28:30 2018

@author: Ni He
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sqlalchemy import create_engine
#import pymysql
import time
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import requests
import re
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class crawlhandler(object): 
    def __init__(self):
        self.host = "10.23.0.2"
        self.port = 3306
        self.user = "root"
        self.pw = "11031103"
        self.charset = "utf8"
        self.sql_eng = 'mysql+mysqldb://root:11031103@10.23.0.2:3306/cnki?charset=utf8'
        self.user_agent = "User-Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'"
        self.urlip = 'http://www.xicidaili.com/nt/' 
        
    def save_into_database_engine(self, table_to_save, table_name):
        engine = create_engine(self.sql_eng) 
        try:
            pd.io.sql.to_sql(table_to_save, table_name, engine, schema = 'cnki', if_exists = 'append', index = False)
        except:
            print('Error in MySQL')
        finally:
            engine.dispose()
    
    def database_execute_engine(self, sql_exec, ret = 0):
        engine = create_engine(self.sql_eng) 
        connection = engine.connect()
        connection.execute(sql_exec)
        if ret == 1:
            return connection
        connection.close()
        engine.dispose()
        
    def load_from_datebase_engine(self, sql_exec):
        engine = create_engine(self.sql_eng) 
        try:
            dat = pd.read_sql_query(sql_exec, engine)
        except:
            print('Cannot find the data')
        finally:
            engine.dispose()
        return dat
        
    def table_exist(self, tab_name):
        conn = self.database_execute_engine('show tables', ret = 1) # 罗列所有当前库里面的所有表格  
        tables = conn.fetchall()
        selectab = re.compile(r'\w*\w*')
        tabnames = selectab.findall(str(tables))
        res = tab_name in tabnames
        return res

    def init_chrome_driver(self, url):
        chrome_options = Options()
        prefs = {'profile.default_content_setting_values':{'images': 2}}  #不加载图片
        chrome_options.add_experimental_option('prefs', prefs) #不加载图片
        #chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument(self.user_agent)  
        #chrome_options.add_argument('-headless')
        #chrome_options.add_argument('-disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        time.sleep(np.random.randint(1,10,1))
        #self.driver = driver
        return driver
    
    def get_ip_list(self):
        web_data = requests.get(self.urlip,headers=self.header)
        soup = BeautifulSoup(web_data.text, 'lxml')
        ips = soup.find_all('tr')
        ip_list = []
        for k in range(1, len(ips)):
            ip_info = ips[k]
            tds = ip_info.find_all('td')
            ip_list.append(tds[1].text + ':' + tds[2].text)
        return ip_list
    #-从代理IP列表里面随机选择一个
    def get_random_ip(self, ip_list):
        proxy_list = []
        for ip in ip_list:
            proxy_list.append('http://' + ip)
        proxy_ip = np.random.choice(proxy_list)
        proxies = {'http': proxy_ip}
        return proxies
    
    
def get_links_in_a_page(driver):
    content = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(content, 'lxml')
    urls = []
    for i in range(len(soup.find_all('dd', class_='clearfix'))):
        href = soup.find_all('dd', class_='clearfix')[i].find('span', class_='name').find('a').get('href')
        url = href.split('&')[1] +'&'+ href.split('&')[2] +'&'+ href.split('&')[3].replace('table','db')
        urls.append('http://kns.cnki.net/kcms/detail/detail.aspx?' + url)
    return urls

def get_links_in_a_journal(front_url):
       
    ds = crawlhandler()
    driver = ds.init_chrome_driver(front_url)
    content = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(content, 'lxml')
    
    #yearissuepage = driver.find_element_by_id(re.compile(r'[0-9]+_Year_Issue'))
    yearissuepage = [x for x in soup.find('div', class_='yearissuepage').text.split('\n') if x != '']
    j_list = pd.DataFrame(columns=['years','issue','url'])
    t = 0
    
    while t <= len(yearissuepage):
        if not 'No' in yearissuepage[t]:  # this is a year
            tmp = pd.DataFrame(columns=['years','issue','url'])
            c_year = yearissuepage[t]
            # click year
            driver.find_element_by_xpath('//*[@id="{}_Year_Issue"]/dt'.format(c_year)).click()
            time.sleep(np.random.randint(1,10,1))
            # the first issue does not need to be click, it is by default
            t = t + 1  # extra skip here
            c_issue = yearissuepage[t].split('.')[1]
            tmp['url'] = get_links_in_a_page(driver)
            tmp['years'] = c_year
            tmp['issue'] = c_issue
            j_list = pd.concat([j_list, tmp], axis = 0, ignore_index = True)
            t = t + 1
            print('start collect year %s ...' % c_year)
        else:
            tmp = pd.DataFrame(columns=['years','issue','url'])
            c_issue = yearissuepage[t].split('.')[1]
            # click issue
            driver.find_element_by_xpath('//*[@id="yq{}"]'.format(c_year+c_issue)).click()
            time.sleep(np.random.randint(1,10,1))
            tmp['url'] = get_links_in_a_page(driver)
            tmp['years'] = c_year
            tmp['issue'] = c_issue
            j_list = pd.concat([j_list, tmp], axis = 0, ignore_index = True)
            t = t + 1
    
    return j_list
    


front_url = 'http://navi.cnki.net/knavi/JournalDetail?pcode=CJFD&pykm=JJYJ'
j_urls = get_links_in_a_journal(front_url)
#journal_list = pd.DataFrame(columns=['years','issue','url', 'title', 'authors', 'emails', 'institute',
                                     'fund','cate','keys','abstract','cites'])
ds = crawlhandler()
ds.save_into_database_engine(j_urls, 'economic_research_journal')
