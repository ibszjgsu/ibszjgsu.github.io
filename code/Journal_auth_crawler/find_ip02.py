# -*- coding: utf-8 -*-
"""
# -*- coding: utf-8 -*-

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
from random import choice 

def get_ip():
    '''获取代理IP'''
    url = 'http://www.xicidaili.com/nn'
    my_headers = {
        'Accept': 'text/html, application/xhtml+xml, application/xml;',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Referer': 'http: // www.xicidaili.com/nn',
        'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 45.0.2454.101Safari / 537.36'
    }
    r = requests.get(url,headers=my_headers)
    soup = BeautifulSoup(r.text,'html.parser')
    data = soup.find_all('td')

    #定义IP和端口Pattern规则
    ip_compile = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')  #匹配IP
    port_compile = re.compile(r'<td>(\d+)</td>')  #匹配端口
    ip = re.findall(ip_compile,str(data))    #获取所有IP
    port = re.findall(port_compile,str(data))  #获取所有端口
    z = [':'.join(i) for i in zip(ip,port)]  #列表生成式
    #print(z)
    #组合IP和端口
    return z

def get_ip_kuaidaili():
    '''从快代理获取代理IP'''
    url = 'https://www.kuaidaili.com/free/inha/1/'
    my_headers = {
        'Accept': 'text/html, application/xhtml+xml, application/xml;',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Referer': 'https://www.kuaidaili.com/free/inha/',
        'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 45.0.2454.101Safari / 537.36'
    }
    r = requests.get(url,headers=my_headers)
    soup = BeautifulSoup(r.text,'html.parser')
    ip_list = [ip.text for ip in soup.find_all(attrs={"data-title": "IP"})]
    port_list = [port.text for port in soup.find_all(attrs={"data-title": "PORT"})]
    z = [':'.join(i) for i in zip(ip_list,port_list)] 
    
    #print(z)
    #组合IP和端口
    return z

def get_ip_youdaili():
    # from 有代理
    url = 'http://www.youdaili.net/Daili/http/'
    my_headers = {
    'Accept': 'text/html, application/xhtml+xml, application/xml;',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 45.0.2454.101Safari / 537.36'
    }
    r = requests.get(url,headers=my_headers)
    soup = BeautifulSoup(r.text,'html.parser')
    latest_paper_url = soup.find(class_='chunlist').find('a').get('href')
    r = requests.get(latest_paper_url,headers=my_headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text,'html.parser')
    return [ip.text.split('@')[0] for ip in soup.find(class_ = 'content').find_all('p')]

# 设置user-agent列表,每次请求时，随机挑选一个user-agent

ua_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
        "Opera/8.0 (Windows NT 5.1; U; en)",
        "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    ]

def get_headers(host_url):
    hp = {}
    try:
        ip = choice(get_ip())
    except:
        return False
    else:
        #指定代理IP
        hp['proxies'] = {
            'http':ip
        }
        hp['headers'] = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': host_url,
#            'Origin': 'https: // best.zhaopin.com',
#            'Referer':'https//best.zhaopin.com/?sid=121128100&site=sou',
            'User-Agent':choice(ua_list)
        }
        
    test_url = 'http://ip.chinaz.com/'
    try:
        res = requests.get(test_url, timeout = 30, headers = hp['headers'], proxies = hp['proxies'])
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        if soup.find(class_='fz24').text == hp['proxies']['http'].split(':')[0]:
#            res = requests.get(host_url, timeout = 30, headers = hp['headers'], proxies = hp['proxies'])
#            res.encoding = 'utf-8'
            return hp
        else:
            get_headers(host_url)
    except:
        get_headers(host_url)
        

host_url = 'www.sciencedirect.com'

ip = choice(get_ip())
ip = {'http': 'http://221.12.10.219:8080',
      'https': 'https://221.12.10.218:443'
      }
import urllib
import socket
socket.setdefaulttimeout(3)

proxy = {'http': '115.215.49.67:30006'}
url = "http://ip.chinaz.com/getip.aspx"
url2 = 'http://icanhazip.com/'

try:
    #res = urllib.urlopen(url,proxies=ip).read()
    res = requests.get(url, timeout = 10, proxies = ip)
    print(res.text)
except:
    print('It is not accessable')

