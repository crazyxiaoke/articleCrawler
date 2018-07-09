#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import traceback
import telnetlib
import common
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
}

url = 'http://www.xicidaili.com/nn/{0}'


def start():
    proxy_list = get_proxy_id()
    check_proxy_usable(proxy_list)


def get_proxy_id(page=1):
    proxy_list = []
    res = requests.get(url.format(page), headers=headers)
    try:
        soup = BeautifulSoup(res.text, 'html.parser')
        trs = soup.find_all('tr', attrs={'class': 'odd'})
        for tr in trs:
            proxy = {}
            tds = tr.find_all('td')
            print(tds[1].text, tds[2].text, tds[5].text)
            proxy['ip'] = tds[1].text
            proxy['port'] = tds[2].text
            proxy['type'] = tds[5].text
            proxy_list.append(proxy)
        pass
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    return proxy_list


def check_proxy_usable(proxys):
    if proxys:
        for proxy in proxys:
            try:
                print("=========开始验证proxy=========")
                print(proxy['ip'], proxy['port'], proxy['type'])
                telnetlib.Telnet(proxy['ip'], port=proxy['port'], timeout=20)
            except Exception:
                print("=========验证proxy失败=========")
                print('')
                continue
            else:
                common.save_proxy_ip('config/proxy_ip', "ip=%s,port=%s,type=%s" % (proxy['ip'], proxy['port'], proxy['type']))
                print("=========验证成功=========")
                print('')
    print("=========验证完成=========")


if __name__ == '__main__':
    start()
