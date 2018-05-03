# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 12:54:59 2018

@author: Ni He
"""

import urllib.request
from bs4 import BeautifulSoup
import re
import requests

def get_html(url):
    #获取请求头，以浏览器身份查看网页信息
    headers = ("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    html = opener.open(url).read()
    html = html.decode("gbk","ignore")
    return html


pagecontent = requests.get('https://www.sciencedirect.com/science/article/pii/S0304407618300587')
                #利用BeautiSoup库将HTML文档格式化
soup = BeautifulSoup(pagecontent.text, 'lxml')
soup2 = BeautifulSoup(pagecontent, 'html.parser')
                #利用BeautiSoup库中的find_all(div,attr)函数定位到股票数据的表格
table = soup2.find_all('mailto')