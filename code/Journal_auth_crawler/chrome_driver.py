# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 17:00:32 2018

@author: Administrator
"""

#  http://npm.taobao.org/mirrors/chromedriver/   chromedriver 镜像下载

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

#driver = webdriver.Chrome(executable_path='C:/ProgramData/Anaconda3/selenium/webdriver/chromedriver/chromedriver.exe', chrome_options=chrome_options)
driver = webdriver.Chrome(chrome_options=chrome_options)

print('start testing...')
time_start = time.time()
driver.get('https://www.sciencedirect.com/')
print(driver.title)

print('Closing')
driver.close()
print('It takes %s seconds.' % (time.time()-time_start))