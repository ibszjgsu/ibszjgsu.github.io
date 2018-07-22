# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 22:26:39 2018

@author: Administrator
"""
import requests
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver


url = 'http://quotes.money.163.com/f10/jjcg_000812.html#01d03'

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
        }


res = requests.get(url, headers = headers)
res.encoding = 'utf-8'

#html = etree.HTML(res.text)
#html_data = html.xpath('//*[@id="2010-12-31"]/table/tbody/tr[13]/td[1]/a')

soup = BeautifulSoup(res.text, 'html.parser')

col_name = soup.find(class_ = 'dbrow').text.strip().split('\n')


info = soup.find_all(class_="table_bg001 border_box limit_sale")
infos = info[0].find_all('td')
infolist = [infos[i].text for i in range(len(infos))]

fund_hold = {}
fund_hold['share_name'] = []
fund_hold['share_code'] = []
for ind in range(len(col_name)):
    fund_hold[col_name[ind]] = infolist[ind::len(col_name)]




listofdate = soup.find_all('form', attrs={'name': 'date'})
if listofdate:
    listofdate = listofdate[0].find_all('option')
    dates = [listofdate[i].text for i in range(len(listofdate))]
    
driver = webdriver.Firefox(executable_path='C:\Program Files (x86)\Mozilla Firefox\geckodriver.exe')
driver.get(url)

dr = driver.find_elements_by_tag_name('option')

dr[3].click()

soup = BeautifulSoup(driver.page_source.encode('utf-8'), 'html.parser')

info = soup.find_all(class_="table_bg001 border_box limit_sale")
owners = info[0].find_all(class_="align_l")
owners = [owners[i].text for i in range(len(owners))]