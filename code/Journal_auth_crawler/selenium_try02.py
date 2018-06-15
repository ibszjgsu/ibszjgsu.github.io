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
    

# Find and click to expand all issues
driver = webdriver.Firefox(executable_path='C:\Program Files (x86)\Mozilla Firefox\geckodriver.exe')
driver.get(jou_all_issue_url)

clickable_links = soup.find_all(class_='accordion-panel js-accordion-panel')

for i in range(len(clickable_links)):
    if clickable_links[i].find('button').get('aria-expanded') == 'false':
        driver.find_element_by_id('0-accordion-tab-' + str(i)).click()
        


expanded_res_issue = driver.page_source.encode('utf-8')
#driver.close()
soup = BeautifulSoup(expanded_res_issue, 'html.parser')
urls = soup.find_all(class_='anchor text-m')
print(len(urls))



#chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe" 
#driver2 = webdriver.Chrome(chromedriver)
#
#journal_url = 'https://www.sciencedirect.com/science/journal/00014575'
#
#driver2.get(journal_url)

