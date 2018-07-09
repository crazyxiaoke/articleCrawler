#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import common
import requests
import time
import random
import json
import traceback
from bs4 import BeautifulSoup
from Article import Article
from mysql import Mysql

'''
    众悦学车网/技巧解析
'''
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
}

url = 'http://www.zyue.com/jiqiao/{0}/list{1}.html'
titles = ['jiaoguimiji', 'daocheruku', 'podaodingdian', 'cefangtingche', 'quxianxingshi', 'zhijiaozhuanwan',
          'daolujiashi', 'anquanwenmingjiashi']
types = {'jiaoguimiji': 6, 'daocheruku': 7, 'podaodingdian': 7, 'cefangtingche': 7, 'quxianxingshi': 7,
         'zhijiaozhuanwan': 7, 'daolujiashi': 8, 'anquanwenmingjiashi': 8}
page = 1  # 初始页数
titleIndex = 0  # 初始标题


def start():
    print('=============开始抓取==============')
    try:
        if os.path.exists('config/next_page.json'):
            next_page_file = open('config/next_page.json', 'r')
            next_page = json.load(next_page_file)
            parseListHtml(next_page['page'], next_page['title'])
        else:
            parseListHtml(page, titleIndex)
    except Exception as e:
        print(e)
    print('=============抓取完成==============')


# 获取文章列表
def parseListHtml(page, titleindex):
    next_page = {'page': page, 'title': titleindex}
    common.save_now_page(next_page)
    mysql = Mysql()
    s = ''
    if page > 1:
        s = '_' + repr(page)
    print(url.format(titles[titleindex], s))
    try:
        response = requests.get(url.format(titles[titleindex], s),
                                headers=headers,
                                timeout=10)
        response.encoding = 'gb2312'
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            re_coms = soup.find_all('ul', attrs={'class': 'recom_list'})
            articles = []
            for re_com in re_coms:
                article = Article(re_com.a.string, re_com.find('span', attrs={'class': 'gd1'}).a.attrs['href'])
                article.author = 'OK学车'
                article.contentHead = parseContentHead(re_com.find('li', attrs={'class': 'recom_nr'}).text)
                article.type = types[titles[titleindex]]
                articles.append(article)
            parseArticle(articles)
            # 保存到数据库
            mysql.insert_array(articles)
            mysql.close()
            # common.save_file(titles[titleIndex], '第{0}页'.format(page), repr(common.convert_to_dicts(articles)))
            sleep_time = random.randint(5, 10)
            print('休息', sleep_time, 's后再获取')
            time.sleep(sleep_time)
            parseListHtml(page + 1, titleindex)
        else:
            mysql.close()
            if titleindex + 1 < len(titles):
                parseListHtml(1, titleindex + 1)
    except Exception as e:
        print(traceback.format_exc())
        print('网页获取失败：', e)
        mysql.close()
        sleep_time = random.randint(1, 5)
        print(repr(sleep_time), 's后重新获取')
        time.sleep(sleep_time)
        parseListHtml(page + 1, titleindex)


# 获取文章内容
def parseArticle(articles):
    for article in articles:
        response = requests.get(article.url, headers=headers)
        response.encoding = 'gb2312'
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            jq_con = soup.find('div', attrs={'class': 'jqcon'})
            new_fl = jq_con.find('div', attrs={'class': 'newfl'})
            if new_fl:
                new_fl.decompose()  # 删掉底部分类标签
            about_new = jq_con.find('div', attrs={'class', 'about_new'})
            if about_new:
                about_new.decompose()  # 删掉关于
            article.content = parseContent(repr(jq_con))


def parseContent(content):
    content.replace(
        u'<p style="text-align: center"><span style="color: #ff0000"><strong><span style="span-: small">众悦原创，转载请注明</span></strong></span></p>',
        '')
    soup = BeautifulSoup(content, 'html.parser')
    soup.div.attrs['class'] = ''
    return repr(soup)


def parseContentHead(contentHead):
    if contentHead:
        soup = BeautifulSoup(contentHead, 'html.parser')
        return soup.text.replace('[阅读全文]', '')
