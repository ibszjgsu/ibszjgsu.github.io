# -*- coding: utf-8 -*-
"""
Created on Mon May 14 14:11:57 2018

@author: Administrator
"""

import requests
import json
import re
import random
import sys
import time
import datetime  #处理日期和时间的标准库
import threading  #引入多线程
from random import choice  #choice() 方法返回一个列表，元组或字符串的随机项
from bs4 import BeautifulSoup


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
    print(z)
    #组合IP和端口
    return z

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

def get_url(url,code=0,ips=[]):
    '''
    投票
    如果因为代理IP已失效造成投票失败，则会自动换一个代理IP后继续投票
    :param code:
    :param ips:
    :return:
    '''
    try:
        ip = choice(ips)
    except:
        return False

    else:
        #指定代理IP
        proxies = {
            'http':ip
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'best.zhaopin.com',
            'Origin': 'https: // best.zhaopin.com',
            'Referer':'https//best.zhaopin.com/?sid=121128100&site=sou',
            'User-Agent':choice(ua_list)
        }

    try:
        data = {"bestid": "15616", "score": "5,5,5,5,5,5","source": "best",}

        result = requests.post(url=url, data=data, proxies=proxies)  # 跳过证书的验证 verify=False
    except requests.exceptions.ConnectionError:
        print('ConnectionError')
        if not ips:
            print('ip 已失效')
            sys.exit()
        #删除不可用的代理IP
        if ip in ips:
            ips.remove(ip)
        #重新请求url
        get_url(url,code=0,ips=[])
    else:
        date = datetime.datetime.now().strftime('%H:%M:%S')
        # result.text() 投票成功显示1  失败显示0
        print(u"第%s次 [%s] [%s]：投票%s (剩余可用代理IP数：%s)" % (code, date, ip, result.text, len(ips)))

def get_num(num):
    #点赞的请求
    url1 = 'https://best.zhaopin.com/API/Vote.ashx'
    #投票的请求
    url2 = 'https://best.zhaopin.com/API/ScoreCompany.ashx'
    if num == 1:
        url=url1
        main(url)
    elif num == 2:
        url =url2
        main(url)
    else:
        print('您的输入有误，请重新输入！！！')
        num = int(input('自主刷赞请选1，自动投票请选2：'))
        get_num(num)


def main(url):
    ips = []
    #xrange() 生成的是一个生成器
    for i in range(6000):
        # 每隔1000次重新获取一次最新的代理IP，每次可获取最新的100个代理IP
        if i % 1000 == 0:
            ips.extend(get_ip())
            print('--------------------------------------')
            print(ips)
        #启动线程，每隔1s产生一个线程，可通过控制时间加快投票速度
        t1 = threading.Thread(target=get_url,args=(url,i,ips))
        t1.start()
        time.sleep(1)  #time.sleep的最小单位是毫秒


if __name__ == '__main__':
    print('欢迎使用自助刷票小工具QAQ')
    num = int(input('自主刷赞请选1，自动投票请选2：'))
    get_num(num)