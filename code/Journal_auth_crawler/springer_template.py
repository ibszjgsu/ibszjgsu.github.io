# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 17:45:50 2018

@author: Ni He

数据库表格的名字需要修改 ejos 一共 三处
中断处理办法：读出中断时候的i和pg； 将第96行附近的循环中的i从中断i开始，运行一次；
修改i回到原始状态( for i in range(0,len(paper_suburls)))；将65行附近的循环中的pg从中断pg+1运行到结束；
"""

import requests
from lxml import etree
import re
import mysql.connector
import time
from bs4 import BeautifulSoup

headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) \
           AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
          }

pageurl ='https://link.springer.com/journal/volumesAndIssues/41265'
res = requests.get(pageurl,timeout=15,headers=headers)
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'html.parser')
sp = soup.find_all('a', class_='title')
links = []
info_date_issue = []
for link in sp:
    links.append(link.get('href'))
    info_date_issue.append(link.get_text())
    
    
    
pageurl2 = 'https://link.springer.com/journal/41265/33/1/page/1'
res2 = requests.get(pageurl2,timeout=15,headers=headers)
res2.encoding = 'utf-8'
soup2 = BeautifulSoup(res2.text, 'html.parser')
sp2 = soup2.find_all('h3', class_='title')
    
for i in range(len(sp2)):
    if 'Research Article' in soup2.find_all('p', class_='content-type')[i]:
        suburl = sp2[i].prettify().split('href="')[1].split('"')[0]
    


pageurl3 = 'https://link.springer.com/article/10.1057/s41265-016-0034-2'
res3 = requests.get(pageurl3,timeout=15,headers=headers)
res3.encoding = 'utf-8'
soup3 = BeautifulSoup(res3.text, 'html.parser')
sp2 = soup3.find_all('span', class_='authors-affiliations__name') # author list
    soup3.find_all('a', class_='gtm-email-author')  # email
    soup3.find('h1', class_='ArticleTitle').get_text()  # title 
    soup3.find(class_="test-metric-count c-button-circle gtm-citations-count").get_text()  # citation
    soup3.find('span', class_="ArticleCitation_Volume").get_text().split(',')[0].strip('Volume').strip() # volume
    soup3.find('time').get_text()  # date
    soup3.find('a', class_="ArticleCitation_Issue").get_text()[-1] # issue
    soup3.find(class_="JournalTitle").get_text()  # joural title
    
    #soup3.find(id="citations-count-number").get_text()     # citation
    #soup3.select('#citations-count-number')[0].get_text()  # citation
    #soup3.find(id = 'Par1', class_="Para").get_text() # abstract
    #soup3.find_all('span', class_="Keyword") # keyword
    
    

def table_exist(tab_name):
    cur.execute('show tables')  # 罗列所有当前库里面的所有表格
    tables = cur.fetchall()
    selectab = re.compile(r'\w*\w*')
    tabnames = selectab.findall(str(tables))
    res = tab_name in tabnames
    return res

#连接MySQL数据库
conn = mysql.connector.connect(host="10.23.0.2",port=3306,user="root",\
                       password="11031103",database="journalcontact",charset="utf8")
cur = conn.cursor()
#==============================================================================
# 
# <<<<<<< HEAD
# if not table_exist('econometricreviews'):
#     #build a new table named by the journal title 
#     sql = "create table econometricreviews (id int not null unique auto_increment, \
# =======
#==============================================================================
if not table_exist('journalofappliedstatistics'):
    #build a new table named by the journal title 
    sql = "create table journalofappliedstatistics (id int not null unique auto_increment, \
         title varchar(300), authors varchar(300), au_email varchar(500),\
         citation varchar(20), volume varchar(20), issue varchar(20), year varchar(20), url varchar(300),\
         primary key(id))"
    cur.execute(sql)


header = {'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'}


# Get the total number of pages of this journal

#firsturl = 'http://apps.webofknowledge.com/summary.do?product=UA&colName=&qid=1415&SID=8AdkR7zG2CwWT9yxRWs&search_mode=GeneralSearch&formValue(summary_mode)=GeneralSearch&update_back2search_link_param=yes&page=1'
#res = requests.get(firsturl,headers=headers)
#selector = etree.HTML(res.text)


pageurlprefix = 'http://apps.webofknowledge.com/'
pageurlsuffix = '&cacheurlFromRightClick=no'
# Store the total page number in pagenum
#pagenum = int(selector.xpath('//*[@id="pageCount.top"]/text()')[0])

"""
需要修改
"""
#==============================================================================
# <<<<<<< HEAD
# pagenum = 22
# pageurl ='http://apps.webofknowledge.com/summary.do?product=WOS&colName=WOS&qid=725&SID=7ALod42x6iSgCGE4XTF&search_mode=GeneralSearch&formValue(summary_mode)=GeneralSearch&update_back2search_link_param=yes&page='
# 
# 
# =======
#==============================================================================
pagenum = 66
pageurl ='https://link.springer.com/journal/volumesAndIssues/41265'



for pg in range(34,pagenum + 1):
    # Next page URL, being used before the end of this loop
    nexturl = pageurl + str(pg)
    # Proceeds to next page by using nexturl
    res = requests.get(pageurl,timeout=15,headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    selector = etree.HTML(res.text)
    
    time_start = time.time()
    # Find the list of paper URLs, store in paper_suburls
    paper_suburls_pat = '<a class="smallV110" href="(.*?)"'
    paper_suburls = re.findall(paper_suburls_pat,res.text)
    # Find the list of paper titles, store in paper_titles
    paper_titles_pat = '<value lang_id="">(.*?)</value>'
    paper_titles = re.findall(paper_titles_pat,res.text)
#    # Find the list of Volume
    paper_vols_pat = 'Volume\: </span><span class="data_bold">\n<value>(.*?)</value>'
    paper_vols = re.findall(paper_vols_pat,res.text)
#    # Find the list of Issue
    paper_iss_pat = 'Issue\: </span><span class="data_bold">\n<value>(.*?)</value>'
    paper_iss = re.findall(paper_iss_pat,res.text)
#    # Find the list of Pages
#    paper_pages_pat = 'Pages: </span><span class="data_bold"> <value>(.*?)</value>'
#    paper_pages = re.findall(paper_pages_pat,res.text, re.S)   
#    # Find the list of Date
    paper_dates_pat = 'Published\: </span><span class="data_bold">\n<value>(.*?)</value>'
    paper_dates = re.findall(paper_dates_pat,res.text)

    # Find the list of Authors
    paper_auths_pat = 'By: </span>(.*?)</div>'
    paper_auths = re.findall(paper_auths_pat,res.text, re.S)
    
    
    for i in range(0,len(paper_suburls)):
        # Clean up the suburl
        suburl = paper_suburls[i].replace('&amp','')
        paper_suburl = pageurlprefix+suburl.replace(';','&')+pageurlsuffix
        # 
        subres = requests.get(paper_suburl,timeout=15,headers=headers)
        subselector = etree.HTML(subres.text)
        
        # Find the list of Number of citation
        paper_cites_pat = '<span class="large-number">(.*?)</span>'
        paper_cites = re.findall(paper_cites_pat,subres.text)
        if len(paper_cites) == 0:
            cites = 0
        else:
            cites = paper_cites[0]
        
        # Find the list of Email address
        paper_email_pat = '<a href="mailto:(.*?)">'
        paper_email = re.findall(paper_email_pat,subres.text)
        if len(paper_email) > 1:
            paper_email = ','.join(paper_email)
        elif len(paper_email) == 1:
            paper_email = paper_email[0]
            
        if i >= len(paper_iss):
            iss = 'NULL'
        else:
            iss = paper_iss[i]
        # Store the data into Database
#==============================================================================
# <<<<<<< HEAD
#         sql_ins = "insert into econometricreviews (title, authors, au_email, citation, volume, issue, year, url) \
# =======
#==============================================================================
#  >>>>>>> f1d91706b06feaf187937072f5d89fe7e7267133        
        sql_ins = "insert into journalofappliedstatistics (title, authors, au_email, citation, volume, issue, year, url) \
        values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %\
        (paper_titles[i].replace("'","").replace('"',''), paper_auths[i].replace("'","").replace('"',''), paper_email, cites,\
         paper_vols[i] or 'NULL', iss or 'NULL', paper_dates[i] or 'NULL', paper_suburl)

        cur.execute(sql_ins)
        conn.commit() 
        time.sleep(3)#睡眠2秒  

    
    # Show the progress... 
    print('Page %s out of %s has been stored.. it takes %s secs.' % (str(pg), str(pagenum), time.time()-time_start))
    # End of loop 
    
    
    #  cur.execute('drop table jsas')
    





























