# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 00:08:00 2018

@author: Administrator
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
import re
import mysql.connector
import time
from bs4 import BeautifulSoup

headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) \
           AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
          }

# Start from the journal ID
journal_url = 'https://www.sciencedirect.com/science/journal/00014575' #00014575 21735735

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
    #driver.close()
    # Parser the new page by BeautifulSoup again to get the links
    soup = BeautifulSoup(expanded_res_issue, 'html.parser')
    # The class of links
    urls = soup.find_all(class_='anchor text-m')
    for url in urls:
        # Get the links by access Tag href
        url_list.append('https://www.sciencedirect.com' + url.get('href'))




