# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 16:55:49 2018

@author: Ni He
"""

from selenium import webdriver            
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.options import Options 
import time, requests, re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

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
        
    def table_exist(self, tab_name):
        conn = self.database_execute_engine('show tables', ret = 1) # 罗列所有当前库里面的所有表格  
        tables = conn.fetchall()
        selectab = re.compile(r'\w*\w*')
        tabnames = selectab.findall(str(tables))
        res = tab_name in tabnames
        return res

    def download_chrome_driver(self, url):
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


def get_journal_list():
    start_url = 'http://navi.cnki.net/knavi/Journal.html'
    ds = crawlhandler()
    driver = ds.download_chrome_driver(start_url)
    # create table 
    tab_name = 'journal_list4'
    #if not ds.table_exist(tab_name):
    sql = 'create table %s(id int auto_increment,\
            title varchar(800), institute varchar(100), freq varchar(50), issn varchar(100), cn varchar(100),\
            location varchar(100), lang varchar(100), psize varchar(100), friyear varchar(100), spec_vol varchar(100),\
            spec_topic varchar(100), num varchar(100), download varchar(100), cite varchar(100), multi_f varchar(100), \
            comp_f varchar(100), honor varchar(200), indexing varchar(600), url varchar(250),\
            PRIMARY KEY(id))' % tab_name 
                #engine.execute(sql)
    ds.database_execute_engine(sql)
    # 点击学术期刊
    driver.find_element_by_xpath('//*[@id="rightnavi"]/ul/li[2]/a').click()
    time.sleep(np.random.randint(5,10,1))
    # 选择核心期刊
    driver.find_element_by_xpath('//*[@id="rightnavi"]/div/div[1]/div/div[1]/a').click()
    # start to collect, 94 pages in total
    p = 94
    while p > 0:
        p = p - 1
        content = driver.page_source.encode('utf-8')
        #time.sleep(np.random.randint(1,10,1))
        soup = BeautifulSoup(content, 'lxml')
        urls = soup.find_all(class_='list_tup')[0].find_all('a')
        # collect in each page
        journal_list = pd.DataFrame(columns=['title', 'url'])
        tmp1 = {}
        for u in urls:
            tmp1['title'] = u.get('title')  # name of journal
            tmp1['url'] = 'http://navi.cnki.net' + u.get('href').split(' ')[-1]  # url
            journal_list = journal_list.append(tmp1, ignore_index=True)
        # finish one page
        
        journal_list_details = pd.DataFrame(columns=['title', 'institute', 'freq', 'issn', 'cn', 'location', 'lang', 'psize',
                                                     'friyear', 'spec_vol', 'spec_topic', 'num', 'download', 'cite', 'multi_f', 'comp_f',
                                                     'honor', 'indexing', 'url'])
        for i in range(len(journal_list)):
            subdriver = ds.download_chrome_driver(journal_list['url'].loc[i])
            # see more about the journal 
            time.sleep(np.random.randint(2,10,1))
            subdriver.find_element_by_xpath('//*[@id="J_sumBtn-stretch"]').click()
            content = subdriver.page_source.encode('utf-8')
            subsoup = BeautifulSoup(content, 'lxml')
            tt = subsoup.find_all(class_='hostUnit')
            tmp = {}
            if '曾用刊名' in tt[0].text:
                s = 1
            else:
                s = 0
            tmp['title']        = journal_list['title'].loc[i]
            tmp['institute']    = tt[s+0].text.split('：')[-1]
            tmp['freq']         = tt[s+1].text.split('：')[-1]
            tmp['issn']         = tt[s+2].text.split('：')[-1]
            tmp['cn']           = tt[s+3].text.split('：')[-1]
            tmp['location']     = tt[s+4].text.split('：')[-1]
            tmp['lang']         = tt[s+5].text.split('：')[-1]
            tmp['psize']        = tt[s+6].text.split('：')[-1]
            if '邮发代号' in tt[s+7].text:
                s = s + 1
            tmp['friyear']      = tt[s+7].text.split('：')[-1]
            tmp['spec_vol']     = tt[s+8].text.split('：')[-1]
            tmp['spec_topic']   = tt[s+9].text.split('：')[-1]
            tmp['num']          = tt[s+10].text.split('：')[-1]
            tmp['download']     = tt[s+11].text.split('：')[-1]
            tmp['cite']         = tt[s+12].text.split('：')[-1]
            tmp['multi_f']      = tt[s+13].text.split('：')[-1]
            tmp['comp_f']       = tt[s+14].text.split('：')[-1]
            tmp['honor']        = tt[-1].text.split(';')[0]
            tmp['indexing']     = subsoup.find_all(id='evaluateInfo')[0].find(class_='more').text.split('期刊荣誉')[0]
            tmp['url']          = journal_list['url'].loc[i]
            
            journal_list_details = journal_list_details.append(tmp, ignore_index=True)
            subdriver.quit()
        if len(journal_list_details) > 0:
            ds.save_into_database_engine(journal_list_details, tab_name)
            print('%d journals in page %d saved at %s' % (len(journal_list_details), p, time.strftime('%Y-%m-%d at %H:%M:%S',time.localtime(time.time()))))            
        # click next page
        driver.find_element_by_xpath('//*[@id="rightnavi"]/div/div[3]/a[13]').click()
    print('Mission completed')
    driver.quit()
        
#if __name__ == "__main__":
#    get_journal_list()
#    
#tab_name = 'journal_list3'
#ds = crawlhandler()
#ds.table_exist(tab_name)        




