# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 16:18:59 2018

@author: Administrator
"""

import requests
import time
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup 
import mysql.connector
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mysql+mysqldb://root:11031103@10.23.0.2:3306/science_direct?charset=utf8') 
#driver = webdriver.Firefox(executable_path='C:\Program Files (x86)\Mozilla Firefox\geckodriver.exe')

#pd.io.sql.to_sql(journal_issue_list, 'journal_issue_list', engine, schema='science_direct', if_exists='append') 
# ret2 = pd.read_sql_query("select id,iss_url from journal_issue_list ",engine)

#conn = mysql.connector.connect(host="10.23.0.2",port=3306,user="root",\
#                       password="11031103",database="science_direct",charset="utf8")
#cur = conn.cursor 

class HtmlDownloader(object):
    
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
           'Host':'www.sciencedirect.com',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding':'gzip, deflate, br',
           'Accept-Language':'zh-CN,zh;q=0.9',
           'Cache-Control':'max-age=0',
           'Connection':'keep-alive'
           }
        self.timeout = 20
        #self.proxy = 

    def download(self,url):
        if url is None:
            return None
        r = requests.get(url, headers=self.headers, timeout = self.timeout)
        # random delay
        time.sleep(np.random.randint(3,30,1))
        if r.status_code==200:
            r.encoding='utf-8'
            return r.text
        return None
    


import re
class DataSaver(object):
    
    def __init__(self):
        self.host = "10.23.0.2"
        self.port = 3306
        self.user = "root"
        self.pw = "11031103"
        self.charset = "utf8"
     
    def conn_mysql(self, db):
        return mysql.connector.connect(host=self.host,port=self.port,user=self.user, password=self.pw, database=db, charset=self.charset)
    
    def table_exist(self, cur, tab_name):
        cur.execute('show tables')  # 罗列所有当前库里面的所有表格
        tables = cur.fetchall()
        selectab = re.compile(r'\w*\w*')
        tabnames = selectab.findall(str(tables))
        res = tab_name in tabnames
        return res
    
    def get_journal_list(self, table_name = 'sciencedirect_humanity'):
        sql = "select * from %s where status = 0" % table_name
        #conn = mysql.connector.connect(host=self.host,port=self.port,user=self.user, password=self.pw, database='science_direct', charset=self.charset)
        conn = self.conn_mysql('science_direct')
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchall()
    
    def load_into_database(self, journal_name, journal_info): 
        conn = self.conn_mysql('science_direct')
        cur = conn.cursor()
        # build up a table if it doesn't exist
        if not self.table_exist(cur, journal_name.casefold()):
        #build a new table named by the journal title 
            sql = "create table %s (id int not null unique auto_increment, \
            title varchar(300), authors varchar(300), au_email varchar(500),\
            volume varchar(20), issue varchar(20), year varchar(20), page varchar(50), keywords varchar(300),\
            abstract varchar(3000), url varchar(300), primary key(id))" %journal_name
            cur.execute(sql)           
        # check if the airticle has been stored
        sql_find = "select id from %s where title = '%s'"%(journal_name.casefold(), journal_info['article_title'])
        cur.execute(sql_find)
        cnt = cur.fetchone()
        # if the article has been stored, then give up the update by terminate the function
        if cnt is not None:
            return 
        # execute insert
        sql_ins = "insert into %s (title, authors, au_email, volume, issue, page, year, keywords, abstract, url)\
                    values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%\
                    (journal_name, journal_info['article_title'], journal_info['name'], journal_info['emails'], journal_info['volume'], journal_info['issue'], journal_info['page'], journal_info['year'], journal_info['keys'], journal_info['abstract'], journal_info['url'])
                    #para = [dbname, title, auths, emails, citations, volume, issue, dates, abstract]
    
        cur.execute(sql_ins)
        conn.commit() 




class HtmlParser(object):
    
#    def __init__(self):
#        self.driver = driver

    def all_issue_of_a_sd_journal(self,journal_id):
        # Start from the journal ID
        journal_url = 'https://www.sciencedirect.com/science/journal/' + journal_id #00014575 21735735
        try:
            res = HtmlDownloader().download(journal_url)
            soup = BeautifulSoup(res, 'html.parser')
        except:
            return None
    
        # Find all of its issues with their URLs
        pat = soup.find_all(href=re.compile('/issues'))
        if len(pat) > 0 :
            jou_all_issue_url = 'https://www.sciencedirect.com' + pat[0].get('href')
        else:
            jou_all_issue_url = 'https://www.sciencedirect.com' + pat.get('href')
            
        try:
            res_issue = HtmlDownloader().download(jou_all_issue_url) 
            soup = BeautifulSoup(res_issue, 'html.parser')
        except:
            return None
        # Find the number of pages
        if soup.find(class_='pagination-pages-label') == None:
            pg = 1
        else:
            pg = int(soup.find(class_='pagination-pages-label').text.split(' ')[-1])
        
        url_list = []

        driver = webdriver.Firefox(executable_path='C:\Program Files (x86)\Mozilla Firefox\geckodriver.exe')

        for p in range(1, pg+1):
            # access different pages in turn
            jou_all_issue_url_new = jou_all_issue_url + '?page=' + str(p)
            # access the page
            try:
                res_issue = HtmlDownloader().download(jou_all_issue_url_new) 
                soup = BeautifulSoup(res_issue, 'html.parser')
            except:
                pass
            # Find and click to expand all issues
            clickable_links = soup.find_all(class_='accordion-panel js-accordion-panel')
            try:
                driver.get(jou_all_issue_url_new)
            except:
                driver.refresh()
                #driver.get(jou_all_issue_url_new)
            # Click all button in the current page to expand all the issues
            for i in range(len(clickable_links)):
                if clickable_links[i].find('button').get('aria-expanded') == 'false':
                    driver.find_element_by_id('0-accordion-tab-' + str(i)).click()
                    # collect page source from the expanded page
            expanded_res_issue = driver.page_source.encode('utf-8')
            # Parser the new page by BeautifulSoup again to get the links
            soup = BeautifulSoup(expanded_res_issue, 'html.parser')
            # The class of links
            urls = soup.find_all(class_='anchor text-m')
            for url in urls:
                # Get the links by access Tag href
                url_list.append('https://www.sciencedirect.com' + url.get('href'))
        driver.close()
        #driver.quit()
        return url_list

    def papers_in_an_issue(self, issue_url):
        # issue_url should be a single URL
        try:
            res = HtmlDownloader().download(issue_url)
            soup = BeautifulSoup(res, 'html.parser')
        except:
            return None    
        urls = soup.find_all(class_='anchor article-content-title u-margin-top-xs u-margin-bottom-s')
        url_list = []
        for url in urls:
            url_list.append('https://www.sciencedirect.com' + url.get('href'))         
        return url_list
    
    
    
    def collect_from_paper(self, paper_url):
        try:
            res = HtmlDownloader().download(paper_url)
            soup = BeautifulSoup(res, 'html.parser')   
            journal_info = {}
            journal_info['url'] = paper_url
            journal_info['article_title'] = soup.find(class_='svTitle').text
            journal_info['volume'] = soup.find(class_='volIssue').text.split(',')[0].strip().split(' ')[-1]
            journal_info['year'] = soup.find(class_='volIssue').text.split(',')[1].strip().split(' ')[-1]
            journal_info['pages'] = soup.find(class_='volIssue').text.split(',')[2].strip().split(' ')[-1]
            journal_info['name'] = ', '.join([au.text.replace('\'','’') for au in soup.find_all(class_='authorName svAuthor')])
            journal_info['emails'] = ', '.join([e.get('href').split(':')[-1] for e in soup.find_all(class_='auth_mail')])
            journal_info['abstract'] = soup.find(class_='abstract svAbstract ').text.replace('\'','’').replace('\u202f', ' ')
            journal_info['issue'] = 'Null'
            #journal_info['keys'] = soup.find(class_='keyword').text.replace('\'','’')
            # some key words part may missed up with Abbreviations
            journal_info['keys'] = ' '.join([it.find_next().text for it in soup.find_all('h2',class_='svKeywords') if it.text == 'Keywords'])
            journal_info['keys'] = journal_info['keys'].replace('\'','’')
            return journal_info
        except:
            return None

    def collect_from_paper2(self, paper_url):
        try:
            res = HtmlDownloader().download(paper_url)
            soup = BeautifulSoup(res, 'html.parser')     
            journal_info = {}
            journal_info['url'] = paper_url
            journal_info['article_title'] = soup.find(class_='title-text').text.replace('\'','’')
            tmp = soup.find_all(class_='text-xs')
            tmp = tmp[[it for it in range(len(tmp)) if tmp[it].find(title='Go to table of contents for this volume/issue') is not None][0]].text
            journal_info['volume'] = tmp.split(',')[0].split(' ')[-1]
            journal_info['page'] = tmp.split(',')[-1].split(' ')[-1]
            journal_info['year'] = tmp.split(',')[-2].split(' ')[-1]
            if len(tmp.split(',')) == 4:
                journal_info['issue'] = tmp.split(',')[1].split(' ')[-1]
            else:
                journal_info['issue'] = 'Null'
            journal_info['name'] = ', '.join([i.text+' '+j.text for (i,j) in zip(soup.find_all(class_ = 'text given-name'), soup.find_all(class_ = 'text surname'))])
            journal_info['name'] = journal_info['name'].replace('\'','’')
            # email address
            email_pat1 = '"href":"mailto:(.*?)"'
            email_pat2 = '"type":"email"},"_":"(.*?)"'
            if len(re.findall(email_pat1, res)) == 0:
                emails = re.findall(email_pat2, res)
            else:
                emails = re.findall(email_pat1, res)# email
            journal_info['emails'] = ', '.join(emails)
            try:
                journal_info['abstract'] = ' '.join([it.text for it in soup.find(class_ = 'abstract author').find_all('p')]).replace('\'','’').replace('\u202f', ' ')
            except:
                journal_info['abstract'] = 'Null'
            try:
                tmp = [it.find_all(class_='keyword')  for it in soup.find_all(class_='keywords-section') if it.find(class_='section-title').text[:3] in 'Keywords'][0]
                journal_info['keys'] = ', '.join([t.text for t in tmp])
                journal_info['keys'] = journal_info['keys'].replace('\'','’')
            except:
                journal_info['keys'] = 'Null'
            
            return journal_info
        except:
            return None
#    
#if __name__ == "__main__":
#    for j_list in DataSaver().get_journal_list():
#        journal_id = j_list[1].split('/')[-1]
#        journal_name = j_list[0]
#        print('Start to collect information from: ' + journal_name)
#        #journal_name = 'Accounting_Management_and_Information_Technologies'
#        #journal_id = '09598022'
#        url_issue_list = HtmlParser().all_issue_of_a_sd_journal(journal_id)
#        for iss in url_issue_list:  # all issues
#            url_paper_list = HtmlParser().papers_in_an_issue(iss)
#            time_start = time.time()
#            for url in url_paper_list:  # for each issue (volume)
#                journal_info = HtmlParser().collect_from_paper2(url)
#                if journal_info is None:
#                    journal_info = HtmlParser().collect_from_paper(url)
#                if journal_info is not None and (not journal_info['article_title'] == 'Editorial') and (not journal_info['article_title'] == 'Editorial Board'):
#                    DataSaver().load_into_database(journal_name, journal_info)
#
#            print('Papers in one issue has been stored.. it takes %s secs.' % (time.time()-time_start))


class journal_data(object):
    
    def __init__(self):
        self.journal_name = self.get_journal_name()
        self.journal_issue_list = self.get_journal_issue_list()
        self.journal_paper_list = self.get_journal_paper_list()
        
        
    def get_journal_name(self):
        journal_name = pd.DataFrame(columns=['name', 'id', 'read'])
        j_list = DataSaver().get_journal_list()
        journal_name['name'] = [names[0] for names in j_list]
        journal_name['id']= [names[1].split('/')[-1] for names in j_list]
        journal_name['read'] = [names[2] for names in j_list]
        return journal_name
    
    def get_journal_issue_list(self):
        journal_issue_list = pd.DataFrame(columns = ['id','iss_url'])
        for ids in range(0,len(self.journal_name['id'])):
#        for ids in range(531, len(journal_name['id'])):
            tmp_issue_list = pd.DataFrame(columns = ['id','iss_url'])
            tmp_issue_list['iss_url'] = HtmlParser().all_issue_of_a_sd_journal(journal_name['id'][ids])
            tmp_issue_list['id'] = journal_name['id'][ids]
            journal_issue_list = journal_issue_list.append(tmp_issue_list)
        return journal_issue_list
    
    def get_journal_paper_list(self):
        journal_paper_list = pd.DataFrame(columns = ['id', 'vol', 'paper_url'])
        for i, row in self.journal_issue_list.iterrows():
        for i, row in ret2.iterrows():    
            tmp_paper_list = pd.DataFrame(columns = ['id','vol','paper_url'])
            tmp_paper_list['paper_url'] = HtmlParser().papers_in_an_issue(row['iss_url'])
            tmp_paper_list['id'] = row['id']
            try: 
                tmp_paper_list['vol'] = row['iss_url'].split('vol/')[1].split('/')[0]
            except:
                tmp_paper_list['vol'] = None 
            journal_paper_list = journal_paper_list.append(tmp_paper_list)
            print('Paper list from issue #%s has been collected and stored...' % i)
            # store into database for every 100 issues
            if np.mod(i,100) == 0:
                pd.io.sql.to_sql(journal_paper_list, 'journal_paper_list', engine, schema = 'science_direct', if_exists = 'append')
                journal_paper_list = pd.DataFrame(columns = ['id', 'vol', 'paper_url'])
            return journal_paper_list
    


#    for j_list in DataSaver().get_journal_list():
#        journal_id = j_list[1].split('/')[-1]
#        journal_name = j_list[0]
#        print('Start to collect information from: ' + journal_name)
#        #journal_name = 'Accounting_Management_and_Information_Technologies'
#        #journal_id = '09598022'
#        url_issue_list = HtmlParser().all_issue_of_a_sd_journal(journal_id)
#        for iss in url_issue_list:  # all issues
#            url_paper_list = HtmlParser().papers_in_an_issue(iss)