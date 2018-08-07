# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 14:20:43 2018

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
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

'''   
https://blog.csdn.net/guduyishuai/article/details/78988793
'''

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
        self.timeout = 100
        #self.proxy = 

    def download_request(self,url):
        if url is None:
            return None
#        session = requests.Session()
#        retry = Retry(connect=5, backoff_factor=0.5)
#        adapter = HTTPAdapter(max_retries=retry)
#        session.mount('http://', adapter)
#        session.mount('https://', adapter)
        #requests.adapters.DEFAULT_RETRIES = 5
        r = requests.get(url, headers=self.headers, timeout = self.timeout)      
                # random delay
        time.sleep(np.random.randint(3,30,1))    
#        retry = 0
#        while True:
#            retry += 1
#            try:
#                r = requests.get(url, headers=self.headers, timeout = self.timeout)      
#                # random delay
#                time.sleep(np.random.randint(3,30,1))
#            except:
#                pass
##                print('Try %s again for %s time...' % (url, retry)
#                
#            if retry == 10:
#                break   
        if r.status_code==200:
            r.encoding='utf-8'
            return r.text
        return None
    
    def download_chrome_driver(self,url, sleep = 'y'):
        chrome_options = Options()
        #prefs = {"profile.managed_default_content_settings.images": 2}
        #chrome_options.add_experimental_option("prefs", prefs)
        #chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('-headless')
        chrome_options.add_argument('-disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        if sleep == 'y':
            time.sleep(np.random.randint(3,20,1))
        return driver
    
    def download_firefox_driver(self, url, sleep = 'y'):
        driver = webdriver.Firefox(executable_path='C:\Program Files (x86)\Mozilla Firefox\geckodriver.exe')
        driver.get(url)
        if sleep == 'y':
            time.sleep(np.random.randint(3,20,1))
        return driver
        

def init_db():
    global engine 
    engine = create_engine('mysql+pymysql://root:11031103@10.23.0.2:3306/science_direct?charset=utf8')
    sql = 'select * from sciencedirect_humanity'
    global journal_name_list
    journal_name_list = pd.read_sql_query(sql,engine) 

def save_db(pd_data, param):
    pd.io.sql.to_sql(pd_data, param['table'], engine, schema = param['db'], if_exists = param['if_exists'], index = param['index'])


def collect_paper_info(urls_in_a_journal, jour_name):
    # paper_url_in_a_journal should be a pd contain: 'url_list' which is the url of individual paper
    paper_info = pd.DataFrame(columns=['title', 'authors','au_email','volume','issue','year','page','keywords','abstract', 'url'])
    paper_url_in_a_journal = urls_in_a_journal.loc[:,['vol','paper_url']]
    paper_url_in_a_journal.reset_index(inplace = True)
    paper_url = paper_url_in_a_journal['paper_url'].tolist()
    ts = time.time() 
    i = 0
    while True:
        i += 1
        # try if can be done by requests
        if len(paper_url) == 0:
            break     
        url = paper_url.pop(0)     
        try:
            res = HtmlDownloader().download_request(url)
        except:
            paper_url.append(url)
            continue 
            
        soup = BeautifulSoup(res, 'html.parser')
        tmp_info = {}
        tmp_info['url'] = url
        # if in an abnormal case
        if soup.find(class_='svTitle') is not None:
            try:
                tmp_info = collect_paper_other(tmp_info, soup)
                paper_info = paper_info.append(tmp_info, ignore_index = True)
                print('An abnormal case occur...')
                continue
            except:
                pass
#            continue
        # if in a normal case
        try:
            tmp_info['title'] = soup.find(class_='title-text').text.replace('\'','’')
            # for those "Introduction", "Editor Broad", "Reveiw" etc which has very short title
            if len(tmp_info['title'].split(' ')) < 4:
                continue 
            tmp = soup.find_all(class_='text-xs')
            tmp = tmp[[it for it in range(len(tmp)) if tmp[it].find(title='Go to table of contents for this volume/issue') is not None][0]].text
            tmp_info['volume'] = tmp.split(',')[0].split(' ')[-1]
            tmp_info['page'] = tmp.split(',')[-1].split(' ')[-1]
            tmp_info['year'] = tmp.split(',')[-2].split(' ')[-1]
            if len(tmp.split(',')) == 4:
                tmp_info['issue'] = tmp.split(',')[1].split(' ')[-1]
            else:
                tmp_info['issue'] = 'Null'
            tmp_info['authors'] = ', '.join([i.text+' '+j.text for (i,j) in zip(soup.find_all(class_ = 'text given-name'), soup.find_all(class_ = 'text surname'))])
            tmp_info['authors'] = tmp_info['authors'].replace('\'','’')
            try:
                tmp_info['abstract'] = ' '.join([it.text for it in soup.find(class_ = 'abstract author').find_all('p')]).replace('\'','’').replace('\u202f', ' ')
            except:
                tmp_info['abstract'] = 'Null'
            try:
                tmp = [it.find_all(class_='keyword')  for it in soup.find_all(class_='keywords-section') if it.find(class_='section-title').text[:3] in 'Keywords'][0]
                tmp_info['keywords'] = ', '.join([t.text for t in tmp])
                tmp_info['keywords'] = tmp_info['keywords'].replace('\'','’')
            except:
                tmp_info['keywords'] = 'Null'    
                
            # Check if driver is necessary 
            email_pat1 = '"href":"mailto:(.*?)"'
            email_pat2 = '"type":"email"},"_":"(.*?)"'
            if len(re.findall(email_pat1, res)) == 0:
                emails = re.findall(email_pat2, res)
                tmp_info['au_email'] = ', '.join(emails)
            else:
                emails = re.findall(email_pat1, res)# email
                tmp_info['au_email'] = ', '.join(emails)
            
            if not tmp_info['au_email']:
                print('Has to use Webdriver: %s' % url)
                try:
                    driver = HtmlDownloader().download_chrome_driver(url)
                    content = driver.page_source.encode('utf-8')
                    soup = BeautifulSoup(content, 'lxml')           
                    names = soup.find_all(class_='icon icon-envelope')
                    email = []
                    for n in names:
                        name = n.find_parent('a').get('name')
                        driver.find_element_by_name(name).click()
                        expanded_content = driver.page_source.encode('utf-8')
                        soup_ex = BeautifulSoup(expanded_content, 'html.parser')
                        email.append(soup_ex.find(class_='e-address').text)
                    tmp_info['au_email'] = ', '.join(email)
                    driver.quit()
                except:
                    tmp_info['au_email'] = 'Null'
        
            paper_info = paper_info.append(tmp_info, ignore_index = True)
        except:
            print('The paper can not be retrievaled: %s' % url)
        if np.mod(i,10) == 0 and i > 0 or paper_url_in_a_journal.shape[0] - i < 10:
             # save into database
            param = {'table': jour_name, 'db': 'science_direct', 'if_exists':'append', 'index': False}
            save_db(paper_info, param)
            paper_info = pd.DataFrame(columns=['title', 'authors','au_email','volume','issue','year','page','keywords','abstract', 'url'])
            print('Up to %s papers information has been collected! time per paper %.2f sec' % (i, (time.time()-ts)/i))
    return paper_info   

def collect_paper_other(journal_info, soup):
    
    journal_info['title'] = soup.find(class_='svTitle').text
    journal_info['volume'] = soup.find(class_='volIssue').text.split(',')[0].strip().split(' ')[-1]
    journal_info['year'] = soup.find(class_='volIssue').text.split(',')[1].strip().split(' ')[-1]
    journal_info['pages'] = soup.find(class_='volIssue').text.split(',')[2].strip().split(' ')[-1]
    journal_info['authors'] = ', '.join([au.text.replace('\'','’') for au in soup.find_all(class_='authorName svAuthor')])
    journal_info['au_email'] = ', '.join([e.get('href').split(':')[-1] for e in soup.find_all(class_='auth_mail')])
    journal_info['abstract'] = soup.find(class_='abstract svAbstract ').text.replace('\'','’').replace('\u202f', ' ')
    journal_info['issue'] = 'Null'
    #journal_info['keys'] = soup.find(class_='keyword').text.replace('\'','’')
    # some key words part may missed up with Abbreviations
    journal_info['keywords'] = ' '.join([it.find_next().text for it in soup.find_all('h2',class_='svKeywords') if it.text == 'Keywords'])
    journal_info['keywords'] = journal_info['keywords'].replace('\'','’')
    return journal_info   

def find_journal_name(valid_id,journal_name_list):

    url = 'https://www.sciencedirect.com/science/journal/' + valid_id
    try:
        journal_name = list(journal_name_list['journal_name'].loc[journal_name_list.journal_url == url])
        if list(journal_name) is not None:
            return list(journal_name)[0]
    except:
        print('Invalid journal ID')
           

if __name__ == "__main__":
    init_db()
    paper_url_list = pd.read_sql_query('select * from journal_paper_list',engine)
    
    while True:
        journal_name_list = pd.read_sql_query('select * from sciencedirect_humanity where status = 0', engine)
        if journal_name_list.empty:
            break
            # find the first un-read journal's id code
        first_valid_id = journal_name_list.iloc[0,:]['journal_url'].split('journal/')[1]
            # find the first un-read journal's paper list
        urls_in_a_journal = paper_url_list.loc[paper_url_list.id == first_valid_id]
            # get journal's name
        jour_name = find_journal_name(first_valid_id, journal_name_list)
        print('Start to collect from journal: %s \n' % jour_name)
        print('Total number of papers in this journal is %s' % urls_in_a_journal.iloc[:,0].size)
            # create a new database
        sql = 'create table %s(id int auto_increment,\
            title varchar(800), authors varchar(800), au_email varchar(800), volume varchar(50),\
            issue varchar(20), year varchar(20), page varchar(40), keywords varchar(1000),\
            abstract varchar(5000), url varchar(150), PRIMARY KEY(id))' % jour_name
        engine.execute(sql)

        # update the read information
        sql = "update sciencedirect_humanity set status = 1 where journal_name = '%s'" % jour_name
        engine.execute(sql)
        # get their information
        paper_info = collect_paper_info(urls_in_a_journal, jour_name)

        # print the process
        print('Journal %s has been store into database.' % jour_name)

    
    
    
    
    
    