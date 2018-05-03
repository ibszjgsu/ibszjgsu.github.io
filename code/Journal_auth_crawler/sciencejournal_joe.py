# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 17:45:50 2018

@author: Ni He
"""

import requests
from lxml import etree
import re
import mysql.connector
import time

def table_exist(tab_name):
    cur.execute('show tables')  # 罗列所有当前库里面的所有表格
    tables = cur.fetchall()
    selectab = re.compile(r'\w*\w*')
    tabnames = selectab.findall(str(tables))
    res = tab_name in tabnames
    return res

#连接MySQL数据库
conn = mysql.connector.connect(host="localhost",port=3306,user="root",\
                       password="11031103",database="test",charset="utf8")
cur = conn.cursor()

if not table_exist('joe3'):
    #build a new table named by the journal title 
    sql = "create table joe3 (id int not null unique auto_increment, \
         title varchar(100), authors varchar(100), au_email varchar(100),\
         citation varchar(20), url varchar(100),\
         primary key(id))"
    cur.execute(sql)

headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) \
           AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
          }
firsturl = 'http://apps.webofknowledge.com/Search.do?product=UA&SID=6AnBf29whXROUIxt1yq&search_mode=GeneralSearch&prID=7a28b5ee-cfda-438c-b52a-bcd823128522'
res = requests.get(firsturl,headers=headers)
selector = etree.HTML(res.text)

#http://apps.webofknowledge.com/full_record.do?product=WOS&search_mode=GeneralSearch&qid=4&SID=6A5bnf642Gt788TcuPi&page=1&doc=1&cacheurlFromRightClick=no
pageurlprefix = 'http://apps.webofknowledge.com/'
pageurlsuffix = '&cacheurlFromRightClick=no'
# Store the total page number in pagenum
pagenum = int(selector.xpath('//*[@id="pageCount.top"]/text()')[0])
'''
The following code is only valid for Journal of Econometrics from Vol 189 issue 2 to Vol   issue  
'''
# This is the prefix of page 2, 3,..., pagenum

pageurl ='http://apps.webofknowledge.com/summary.do?product=UA&parentProduct=UA&search_mode=GeneralSearch&parentQid=&qid=1&SID=6AnBf29whXROUIxt1yq&&update_back2search_link_param=yes&page='

for pg in range(17,pagenum + 1):
    # Next page URL, being used before the end of this loop
    nexturl = pageurl + str(pg)
    time_start = time.time()
    # Find the list of paper URLs, store in paper_suburls
    paper_suburls_pat = '<a class="smallV110" href="(.*?)"'
    #paper_suburls_pat = '<span style="display: none" url="(.*?)" id="fetch'
    paper_suburls = re.findall(paper_suburls_pat,res.text, re.S)
    # Find the list of paper titles, store in paper_titles
    paper_titles_pat = '<value lang_id="">(.*?)</value>'
    paper_titles = re.findall(paper_titles_pat,res.text, re.S)
#    # Find the list of Volume
#    paper_vols_pat = 'Volume: </span><span class="data_bold"> <value>(.*?)</value>'
#    paper_vols = re.findall(paper_vols_pat,res.text, re.S)
#    # Find the list of Issue
#    paper_iss_pat = 'Issue: </span><span class="data_bold"> <value>(.*?)</value>'
#    paper_iss = re.findall(paper_iss_pat,res.text, re.S)
#    # Find the list of Pages
#    paper_pages_pat = 'Pages: </span><span class="data_bold"> <value>(.*?)</value>'
#    paper_pages = re.findall(paper_pages_pat,res.text, re.S)   
#    # Find the list of Date
#    paper_dates_pat = 'Published: </span><span class="data_bold"> <value>(.*?)</value>'
#    paper_dates = re.findall(paper_dates_pat,res.text, re.S)
    # Find the list of Number of citation
    paper_cites_pat = '<div class="search-results-data-cite">Times Cited: (.*?)<br>'
    paper_cites = re.findall(paper_cites_pat,res.text, re.S)    
    # Find the list of Authors
    paper_auths_pat = 'By: </span>(.*?)</div>'
    paper_auths = re.findall(paper_auths_pat,res.text, re.S)
    
    
    for i in range(0,len(paper_suburls)):
        # Clean up the suburl
        suburl = paper_suburls[i].replace('&amp','')
        paper_suburl = pageurlprefix+suburl.replace(';','&')+pageurlsuffix
        # 
        subres = requests.get(paper_suburl,headers=headers)
        subselector = etree.HTML(subres.text)
        # Find the list of Email address
        paper_email_pat = '<a href="mailto:(.*?)">'
        paper_email = re.findall(paper_email_pat,subres.text, re.S)
        if len(paper_email) > 1:
            paper_email = ','.join(paper_email)
        elif len(paper_email) == 1:
            paper_email = paper_email[0]
        # Store the data into Database
        sql_ins = "insert into joe3 (title, authors, au_email, citation, url) \
        values ('%s', '%s', '%s', '%s', '%s')" %\
        (paper_titles[i], paper_auths[i], paper_email, paper_cites[i], paper_suburl)
        try:
            cur.execute(sql_ins)
            conn.commit()
        except:
            conn.rollback()  
        time.sleep(1)#睡眠2秒  
 
       
    
    # Proceeds to next page by using nexturl
    res = requests.get(nexturl,headers=headers)
    selector = etree.HTML(res.text)
    
    # Show the progress... 
    print('Page %s out of %s has been stored.. it takes %s secs.' % (str(pg), str(pagenum), time.time()-time_start))
    # End of loop 
    
    
    
    
    
##paper_urls = selector.xpath('//div[@class="anchor article-content-title u-margin-top-xs u-margin-bottom-s"]/a/@href')
#while True:
##for echos in range(0,3):
#    # Find the URL of next page
#    nexturlpat = 'aria-disabled="false" rel="next" href="(.*?)"><span class' 
#    nexturl = 'https://www.sciencedirect.com/' + re.findall(nexturlpat,res.text,re.S)[0]
#    
#    # List of paper sub URl need to be appended by 'https://www.sciencedirect.com/'
#    paper_suburl = selector.xpath('//*[starts-with(@id,"S03044076")]/@href')
#
#    for sub_url in paper_suburl:
#        time_start = time.time()
#        url = 'https://www.sciencedirect.com/' + sub_url
#        res2 = requests.get(url,headers=headers)
#        html = etree.HTML(res2.text)
#        paper_title = html.xpath('//*[@id="ti000005"]/text()')[0]
#        paper_volissue = html.xpath('//*[@id="centerInner"]/div[1]/div[2]/p[1]/a/text()')[0]
#        vol = paper_volissue.split(',')[0].split(' ')[-1]
#        iss = paper_volissue.split(',')[1].split(' ')[-1]
#        sql_ins01 = "insert into joe3 (Vol, Issue, title, url) values ('%s', '%s', '%s', '%s')" %\
#        (vol, iss, paper_title, url)
#        try:
#            cur.execute(sql_ins01)
#            conn.commit()
#        except:
#            conn.rollback()  
#        time.sleep(2)#睡眠2秒    
#        mailpat = '{"type":"email"},"_":"(.*?)"}]}'
#        maillist = re.findall(mailpat,res2.text,re.S)
#        namepat = '<span class="text given-name">(.*?)</span>'
#        author_given_list = re.findall(namepat,res2.text,re.S)
#        namepat = '<span class="text surname">(.*?)</span>'
#        author_sur_list = re.findall(namepat,res2.text,re.S)
#        
#        if len(author_sur_list) == 0:  # if there is no author information then skip
#            continue
#        for i in range(1,len(author_sur_list)+1):
#            if i > 3:  # we only take first 3 authors information
#                break
#            # in case of data missing, fill in na 
#            author_sur = 'na' if len(author_sur_list) < i else author_sur_list[i-1]
#            author_given = 'na' if len(author_given_list) < i else author_given_list[i-1]
#            mlist = 'na' if len(maillist) < i else maillist[i-1]
#            # insert into database
#            sql_tmp = "update joe3 set au_sur_"+str(i)+" = '%s' , au_gen_"+str(i)+"  = '%s', au_email_"+str(i)+" = '%s' where title = '%s'"
#            sql_ins02 = sql_tmp % (author_sur, author_given, mlist, str(paper_title))
#            try:
#               cur.execute(sql_ins02)
#               conn.commit()
#            except:
#               conn.rollback()  
    
     # Program stops if there is no more next page (latest issue)




























