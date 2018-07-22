r# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 17:45:50 2018

@author: Ni He

中断处理办法：读出中断时候的i和k； 将第74行附近的循环中的i从中断i开始，运行一次；
修改i回到原始状态；将63行附近的循环中的k从中断k+1运行到结束；
"""

import requests
#from lxml import etree
import re
import mysql.connector
import time
from bs4 import BeautifulSoup
import os
import csv

#==============================================================================
# 

#dbname = 'journal_of_information_technology'
#journal_id = '41265'
#earliest_year = '2000'

#==============================================================================



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
                       password="11031103",database="journalcontact",charset="utf8")
cur = conn.cursor()

def inf_get_springer(dbname, journal_id, earliest_year = '2000'):
    
    if not table_exist(dbname):
    #build a new table named by the journal title 
        sql = "create table %s (id int not null unique auto_increment, \
        title varchar(300), authors varchar(300), au_email varchar(500),\
        citation varchar(20), volume varchar(20), issue varchar(20), year varchar(20), art_class varchar(100), keywords varchar(300),\
        abstract varchar(3000), url varchar(300), primary key(id))" %dbname
        cur.execute(sql)
    else:
        return

    pageurl ='https://link.springer.com/journal/volumesAndIssues/' + journal_id  # first level URL
    res = requests.get(pageurl,timeout=15,headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    sp = soup.find_all('a', class_='title')
#links = []

    for k in range(61,len(sp)):
        # ignore the publication earlier than certain year
        if int(sp[k].get_text().split(',')[0].split(' ')[-1]) < int(earliest_year):
            continue
        time_start = time.time()
        pageurl2 = 'https://link.springer.com' + sp[k].get('href')
        #links.append(link.get('href'))
        res2 = requests.get(pageurl2,timeout=15,headers=headers)
        res2.encoding = 'utf-8'
        soup2 = BeautifulSoup(res2.text, 'html.parser')
        sp2 = soup2.find_all('h3', class_='title')
        for i in range(0,len(sp2)):
            #if 'Research Article' in soup2.find_all('p', class_='content-type')[i]:
            if True:    
                try:
                    art_class = soup2.find_all('p', class_='content-type')[i].text.replace('\'','’')
                except:
                    art_class = 'Null'    
                suburl = sp2[i].prettify().split('href="')[1].split('"')[0]
                pageurl3 = 'https://link.springer.com' + suburl
                try:
                    res3 = requests.get(pageurl3,timeout=30,headers=headers)
                    res3.encoding = 'utf-8'
                except:
                    print('Oops, something wrong with the journal: %s. @ %s. %s out of %s has been done.' % (dbname, pageurl3, k, len(sp)))
                    #return
                soup3 = BeautifulSoup(res3.text, 'html.parser')
                
                auth_pat = 'class="authors-affiliations__name">(.*?)</span>'
                auths = re.findall(auth_pat, res3.text)   # author list
                auths = ', '.join(auths).replace('\xa0', ' ').replace('\'','’') # merge the list into a string and remove blank
                                 
                email_pat = 'class="authors__contact"><a href="mailto:(.*?)" title='
                emails = re.findall(email_pat, res3.text)  # email
                emails = ', '.join(emails)
                try:
                    title = soup3.find('h1', class_='ArticleTitle').get_text().replace('\'','’')  # title 
                except:
                    title = 'Null'
                try:                
                    citations = soup3.find(class_='test-metric-count c-button-circle gtm-citations-count').get_text()  # citation
                except:
                    citations = 'Null'
                    #cite_pat = "class='test-metric-count c-button-circle gtm-citations-count'>(.*?)</span>"
                    #citations = re.findall(cite_pat, res3.text)
                try:
                    volume = soup3.find('span', class_='ArticleCitation_Volume').get_text().split(',')[0].strip('Volume').strip() # volume
                except:
                    volume = 'Null'
                try:
                    dates = soup3.find('time').get_text()  # date
                except:
                    dates = 'Null'    
                try:
                    issue = soup3.find('a', class_='ArticleCitation_Issue').get_text()[-1] # issue
                except:
                    issue = 'Null'    
                    
                #journal_title = soup3.find(class_="JournalTitle").get_text()  # joural title
                key_pat = '<span class="Keyword">(.*?)</span>'
                keys = re.findall(key_pat, res3.text)  # keyword
                keys = ', '.join(keys).replace('\xa0', '').replace('\'','’')  # clean up keyword
                #soup3.find_all('a', class_='gtm-email-author')  # email
                #soup3.find(id="citations-count-number").get_text()     # citation
                #soup3.select('#citations-count-number')[0].get_text()  # citation
                try:
                    abstract = soup3.find('p', class_="Para").get_text().replace('\'','’') # abstract
                except:
                    abstract = 'Null'                        
                    #soup3.find_all('span', class_="Keyword") # keyword  
            
                sql_ins = "insert into %s (title, authors, au_email, citation, volume, issue, year, art_class, keywords, abstract, url)\
                values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%\
                (dbname, title, auths, emails, citations, volume, issue, dates, art_class, keys, abstract, pageurl3)
                #para = [dbname, title, auths, emails, citations, volume, issue, dates, abstract]
                try:
                    cur.execute(sql_ins)
                    conn.commit() 
                    time.sleep(5)#睡眠2秒  
                except:
                    time.sleep(2)
        print('Volume %s @ year %s has been stored.. it takes %s secs.' % (volume, dates, time.time()-time_start))   
 
#
#db_list = []
#id_list = []

f = csv.reader(open(os.getcwd()+'\\journal_list.csv')) # 读取收件人 邮箱和姓名信息
for rows in f:
#    db_list.append(rows[0])
#    id_list.append(rows[1])
    inf_get_springer(rows[0], rows[1])


#find( name , attrs , recursive , text , **kwargs )
    
#pageurl2 = 'https://link.springer.com/journal/41265/33/1/page/1'  # Second level URL
#res2 = requests.get(pageurl2,timeout=15,headers=headers)
#res2.encoding = 'utf-8'
#soup2 = BeautifulSoup(res2.text, 'html.parser')
#sp2 = soup2.find_all('h3', class_='title')
#    
#for i in range(len(sp2)):
#    if 'Research Article' in soup2.find_all('p', class_='content-type')[i]:
#        suburl = sp2[i].prettify().split('href="')[1].split('"')[0]
#    
#time_start = time.time()
#
#pageurl3 = 'https://link.springer.com/article/10.1057/s41265-016-0034-2'   # Third level URL
#res3 = requests.get(pageurl3,timeout=15,headers=headers)
#res3.encoding = 'utf-8'
#soup3 = BeautifulSoup(res3.text, 'html.parser')
##sp2 = soup3.find_all('span', class_='authors-affiliations__name') # author list
#auth_pat = 'class="authors-affiliations__name">(.*?)</span>'
#auths = re.findall(auth_pat, res3.text)   # author list
#auths = ', '.join(auths).replace('\xa0', ' ') # merge the list into a string and remove blank
#email_pat = 'class="authors__contact"><a href="mailto:(.*?)" title='
#emails = re.findall(email_pat, res3.text)  # email
#emails = ', '.join(emails)
#title = soup3.find('h1', class_='ArticleTitle').get_text()  # title 
#citations = soup3.find(class_="test-metric-count c-button-circle gtm-citations-count").get_text()  # citation
#volume = soup3.find('span', class_="ArticleCitation_Volume").get_text().split(',')[0].strip('Volume').strip() # volume
#dates = soup3.find('time').get_text()  # date
#issue = soup3.find('a', class_="ArticleCitation_Issue").get_text()[-1] # issue
#journal_title = soup3.find(class_="JournalTitle").get_text()  # joural title
#key_pat = '<span class="Keyword">(.*?)</span>'
#keys = re.findall(key_pat, res3.text)  # keyword
#keys = ', '.join(keys).replace('\xa0', '')  # clean up keyword
#    #soup3.find_all('a', class_='gtm-email-author')  # email
#    #soup3.find(id="citations-count-number").get_text()     # citation
#    #soup3.select('#citations-count-number')[0].get_text()  # citation
#    #soup3.find(id = 'Par1', class_="Para").get_text() # abstract
#    #soup3.find_all('span', class_="Keyword") # keyword
#
#
#
#
#
#
#for pg in range(34,pagenum + 1):
#    # Next page URL, being used before the end of this loop
#    nexturl = pageurl + str(pg)
#    # Proceeds to next page by using nexturl
#    res = requests.get(pageurl,timeout=15,headers=headers)
#    res.encoding = 'utf-8'
#    soup = BeautifulSoup(res.text, 'lxml')
#    selector = etree.HTML(res.text)
#    
#    time_start = time.time()
#    # Find the list of paper URLs, store in paper_suburls
#    paper_suburls_pat = '<a class="smallV110" href="(.*?)"'
#    paper_suburls = re.findall(paper_suburls_pat,res.text)
#    # Find the list of paper titles, store in paper_titles
#    paper_titles_pat = '<value lang_id="">(.*?)</value>'
#    paper_titles = re.findall(paper_titles_pat,res.text)
##    # Find the list of Volume
#    paper_vols_pat = 'Volume\: </span><span class="data_bold">\n<value>(.*?)</value>'
#    paper_vols = re.findall(paper_vols_pat,res.text)
##    # Find the list of Issue
#    paper_iss_pat = 'Issue\: </span><span class="data_bold">\n<value>(.*?)</value>'
#    paper_iss = re.findall(paper_iss_pat,res.text)
##    # Find the list of Pages
##    paper_pages_pat = 'Pages: </span><span class="data_bold"> <value>(.*?)</value>'
##    paper_pages = re.findall(paper_pages_pat,res.text, re.S)   
##    # Find the list of Date
#    paper_dates_pat = 'Published\: </span><span class="data_bold">\n<value>(.*?)</value>'
#    paper_dates = re.findall(paper_dates_pat,res.text)
#
#    # Find the list of Authors
#    paper_auths_pat = 'By: </span>(.*?)</div>'
#    paper_auths = re.findall(paper_auths_pat,res.text, re.S)
#    
#    
#    for i in range(0,len(paper_suburls)):
#        # Clean up the suburl
#        suburl = paper_suburls[i].replace('&amp','')
#        paper_suburl = pageurlprefix+suburl.replace(';','&')+pageurlsuffix
#        # 
#        subres = requests.get(paper_suburl,timeout=15,headers=headers)
#        subselector = etree.HTML(subres.text)
#        
#        # Find the list of Number of citation
#        paper_cites_pat = '<span class="large-number">(.*?)</span>'
#        paper_cites = re.findall(paper_cites_pat,subres.text)
#        if len(paper_cites) == 0:
#            cites = 0
#        else:
#            cites = paper_cites[0]
#        
#        # Find the list of Email address
#        paper_email_pat = '<a href="mailto:(.*?)">'
#        paper_email = re.findall(paper_email_pat,subres.text)
#        if len(paper_email) > 1:
#            paper_email = ','.join(paper_email)
#        elif len(paper_email) == 1:
#            paper_email = paper_email[0]
#            
#        if i >= len(paper_iss):
#            iss = 'NULL'
#        else:
#            iss = paper_iss[i]
#        # Store the data into Database
##==============================================================================
## <<<<<<< HEAD
##         sql_ins = "insert into econometricreviews (title, authors, au_email, citation, volume, issue, year, url) \
## =======
##==============================================================================
##  >>>>>>> f1d91706b06feaf187937072f5d89fe7e7267133        
#        sql_ins = "insert into %s (title, authors, au_email, citation, volume, issue, year, url) \
#        values " % dbname
#        (paper_titles[i].replace("'","").replace('"',''), paper_auths[i].replace("'","").replace('"',''), paper_email, cites,\
#         paper_vols[i] or 'NULL', iss or 'NULL', paper_dates[i] or 'NULL', paper_suburl)
#
#        cur.execute(sql_ins)
#        conn.commit() 
#        time.sleep(3)#睡眠2秒  
#
#    
#    # Show the progress... 
#    print('Page %s out of %s has been stored.. it takes %s secs.' % (str(pg), str(pagenum), time.time()-time_start))
#    # End of loop 
#    
#    
#    #  cur.execute('drop table %s'%dbname)
#    





























