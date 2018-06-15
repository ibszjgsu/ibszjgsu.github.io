# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 00:08:00 2018

@author: Ni He
"""
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.by import By
import requests
import re
import mysql.connector
import time
from bs4 import BeautifulSoup
#from random import choice 



headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

    # connect to database
conn = mysql.connector.connect(host="10.23.0.2",port=3306,user="root",\
                       password="11031103",database="science_direct",charset="utf8")
cur = conn.cursor()

def table_exist(tab_name):
    cur.execute('show tables')  # 罗列所有当前库里面的所有表格
    tables = cur.fetchall()
    selectab = re.compile(r'\w*\w*')
    tabnames = selectab.findall(str(tables))
    res = tab_name in tabnames
    return res

def all_issue_of_a_sd_journal(journal_id):
    # Start from the journal ID
    journal_url = 'https://www.sciencedirect.com/science/journal/' + journal_id #00014575 21735735

    res = requests.get(journal_url, timeout = 30, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')

    # Find all of its issues with their URLs
    pat = soup.find_all(href=re.compile('/issues'))
    if len(pat) > 0 :
        jou_all_issue_url = 'https://www.sciencedirect.com' + pat[0].get('href')
    else:
        jou_all_issue_url = 'https://www.sciencedirect.com' + pat.get('href')
    
    res_issue = requests.get(jou_all_issue_url, timeout = 30, headers = headers)
    res_issue.encoding = 'utf-8'
    soup = BeautifulSoup(res_issue.text, 'html.parser')

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
        res_issue = requests.get(jou_all_issue_url_new, timeout = 30, headers = headers)
        res_issue.encoding = 'utf-8'
        soup = BeautifulSoup(res_issue.text, 'html.parser')
        # Find and click to expand all issues
        clickable_links = soup.find_all(class_='accordion-panel js-accordion-panel')
        driver.get(jou_all_issue_url_new)
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
         #driver.close()
    return url_list

def papers_in_an_issue(issue_url):
    # issue_url should be a single URL
    res = requests.get(issue_url, headers = headers, timeout = 30)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    urls = soup.find_all(class_='anchor article-content-title u-margin-top-xs u-margin-bottom-s')
    url_list = []
    for url in urls:
        url_list.append('https://www.sciencedirect.com' + url.get('href'))
        
    return url_list

def collect_from_paper(paper_url):
    
    res = requests.get(paper_url, headers = headers, timeout = 30) 
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    
    journal_info = {}
    try:
        journal_info['url'] = paper_url
        journal_info['article_title'] = soup.find(class_='svTitle').text
        journal_info['volume'] = soup.find(class_='volIssue').text.split(',')[0].strip().split(' ')[-1]
        journal_info['year'] = soup.find(class_='volIssue').text.split(',')[1].strip().split(' ')[-1]
        journal_info['pages'] = soup.find(class_='volIssue').text.split(',')[2].strip().split(' ')[-1]
        journal_info['name'] = ', '.join([au.text.replace('\'','’') for au in soup.find_all(class_='authorName svAuthor')])
        journal_info['emails'] = ', '.join([e.get('href').split(':')[-1] for e in soup.find_all(class_='auth_mail')])
        journal_info['abstract'] = soup.find(class_='abstract svAbstract ').text.replace('\'','’').replace('\u202f', ' ')
        #journal_info['keys'] = soup.find(class_='keyword').text.replace('\'','’')
        # some key words part may missed up with Abbreviations
        journal_info['keys'] = ' '.join([it.find_next().text for it in soup.find_all('h2',class_='svKeywords') if it.text == 'Keywords'])
    except:
        return
    return journal_info


def collect_from_paper2(paper_url):
    
    res = requests.get(paper_url, headers = headers, timeout = 30) 
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    
    journal_info = {}
    try:
        journal_info['url'] = paper_url
        journal_info['article_title'] = soup.find(class_='title-text').text.replace('\'','’')
        tmp = soup.find_all(class_='text-xs')
        tmp = tmp[[it for it in range(len(tmp)) if tmp[it].find(title='Go to table of contents for this volume/issue') is not None][0]].text
        journal_info['volume'] = tmp.split(',')[0].split(' ')[-1]
        journal_info['year'] = tmp.split(',')[1].split(' ')[-1]
        journal_info['pages'] = tmp.split(',')[2].split(' ')[-1]
        journal_info['name'] = ', '.join([i.text+' '+j.text for (i,j) in zip(soup.find_all(class_ = 'text given-name'), soup.find_all(class_ = 'text surname'))])
        # email address
        email_pat1 = '"href":"mailto:(.*?)"'
        email_pat2 = '"type":"email"},"_":"(.*?)"'
        if len(re.findall(email_pat1, res.text)) == 0:
            emails = re.findall(email_pat2, res.text)
        else:
            emails = re.findall(email_pat1, res.text)# email
        journal_info['emails'] = ', '.join(emails)
        try:
            journal_info['abstract'] = ' '.join([it.text for it in soup.find(class_ = 'abstract author').find_all('p')]).replace('\'','’').replace('\u202f', ' ')
        except:
            journal_info['abstract'] = 'Null'
        try:
            tmp = [it.find_all(class_='keyword')  for it in soup.find_all(class_='keywords-section') if it.find(class_='section-title').text[:3] in 'Keywords'][0]
            journal_info['keys'] = ', '.join([t.text for t in tmp])
        except:
            journal_info['keys'] = 'Null'
            
    except:
        return
    return journal_info

def load_into_database(journal_name, journal_info):
    
    # build up a table if it doesn't exist
    if not table_exist(journal_name.casefold()):
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
    sql_ins = "insert into %s (title, authors, au_email, volume, page, year, keywords, abstract, url)\
                values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%\
                (journal_name, journal_info['article_title'], journal_info['name'], journal_info['emails'], journal_info['volume'], journal_info['pages'], journal_info['year'], journal_info['keys'], journal_info['abstract'], journal_info['url'])
                #para = [dbname, title, auths, emails, citations, volume, issue, dates, abstract]
    try:
        cur.execute(sql_ins)
        conn.commit() 
        time.sleep(5)#睡眠2秒  
    except:
        time.sleep(2)
    
    return

# Main function    
#
#def main_fun():
#    journal_name = 'Accident_Analysis_Prevention'
#    journal_id = '00014575'
#    url_issue_list = all_issue_of_a_sd_journal(journal_id)
#    for iss in url_issue_list:  # all issues
#        url_paper_list = papers_in_an_issue(iss)
#        time_start = time.time()
#        for url in url_paper_list:  # for each issue (volume)
#            journal_info = collect_from_paper2(url)
#            if journal_info is None:
#                journal_info = collect_from_paper(url)
#            if journal_info is not None:
#                load_into_database(journal_name, journal_info)
#        print('Papers in one issue has been stored.. it takes %s secs.' % (time.time()-time_start))
#    return
#
#try:
#    main_fun()
#except ConnectionError:
#    time.sleep(100)
#    main_fun()

journal_name = 'Accounting_Forum'
journal_id = '01559982'
url_issue_list = all_issue_of_a_sd_journal(journal_id)
for iss in url_issue_list:  # all issues
    url_paper_list = papers_in_an_issue(iss)
    time_start = time.time()
    for url in url_paper_list:  # for each issue (volume)
        journal_info = collect_from_paper2(url)
        if journal_info is None:
            journal_info = collect_from_paper(url)
        if journal_info is not None and (not journal_info['article_title'] == 'Editorial') and (not journal_info['article_title'] == 'Editorial Board'):
            load_into_database(journal_name, journal_info)
    print('Papers in one issue has been stored.. it takes %s secs.' % (time.time()-time_start))