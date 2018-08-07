# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 01:51:57 2018

@author: Administrator
"""

import requests, re, json, os, urllib
from bs4 import BeautifulSoup

def get_html(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Referer': 'http://music.163.com/',
            'Host': 'music.163.com'
            }
    try:
        response = requests.get(url, headers = headers)
        html = response.text
        return html
    except:
        print('error')
        pass
    
def get_singer_info(soup):
    
    links = soup.find('ul', class_='f-hide').find_all('a')
    song_IDs =[]
    song_names = []
    for link in links:
        song_ID = link.get('href').split('=')[-1]
        song_name = link.get_text()
        song_IDs.append(song_ID)
        song_names.append(song_name)
    return zip(song_names, song_IDs)

#url = 'https://music.163.com/#/search/m/?s=%E6%AE%B7%E7%A7%80%E6%A2%85&type=1'
#//*[@id="auto-id-p1ceZ141W2T4M9Fm"]/div/div/div[1]/div[2]/div/div/a/b
        
def download_song(song_name, song_id):
    singer_url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(song_id)
    print('正在下载歌曲:{}'.format(song_name))
    urllib.request.urlretrieve(singer_url, path + '\\{}.mp3'.format(song_name))
    
if __name__== '__main__':
    singer_id = input('Singer\'s ID:')
    #singer_name = input('歌手姓名：')
 
    start_url = 'http://music.163.com/artist?id={}'.format(singer_id)
    html = get_html(start_url)
    soup = BeautifulSoup(html, 'lxml')
    singer_name = soup.find(id = 'artist-name').text
    singer_infos = get_singer_info(soup)

    path = 'F:\\KuGou\\{}'.format(singer_name)
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
    print('开始下载 %s 的歌曲...' % singer_name)
    for singer_info in singer_infos:
        
        download_song(singer_info[0].split('/')[-1], singer_info[1])
