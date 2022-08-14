#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 测试future方法的threadpool
import os

import requests
from lxml import etree
import sys
import json

from concurrent import futures

MAX_WORKERS = 20
BASE_DIR = 'img_dowload'


def get_url(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
    }
    res = requests.get(url=url, headers=headers)
    return res.text


def get_html(text):
    html = etree.HTML(text)
    return html


def get_script(html):
    # url_list = []
    parse_script_list = html.xpath('//*[@id="data-more"]/text()')
    for p in parse_script_list:
        d = json.loads(p)
        return [p['url'] for p in d]


def xpath_url(html):
    urls_list = []
    parse_ul_list = html.xpath('//*[@id="container"]/ul/li')
    for urls in parse_ul_list:
        parse_li_list = urls.xpath('./div/a')
        for parse_div_list in parse_li_list:
            parse_a_list = parse_div_list.xpath('./@href')
            for i in parse_a_list:
                if i.endswith('.html'):
                    # print(i)
                    urls_list.append(i)
    return urls_list


# 获取第一页的htmls
def get_htmls(base_url):
    text = get_url(url=base_url)
    html = get_html(text)
    urls2 = xpath_url(html)
    urls1 = get_script(html)
    # print(len( urls1 +  urls2))
    return urls1 + urls2


def get_img_url_one(html_url):
    text = get_url(html_url)
    html = get_html(text)
    html_x = html.xpath('//*[@id="imgView"]/@src')[0]
    return {'ref': str(html_url), 'jpgurl': str(html_x)}


def get_img_url_one2(html_url):
    text = get_url(html_url)
    html = get_html(text)
    html_x = html.xpath('//*[@id="imgView"]/@src')[0]
    return html_x


# 进入低一些获取全部的jpgurls
def get_img_urls(htmls_urls):
    return [get_img_url_one2(a) for a in htmls_urls]


def get_img_future(htmls_urls):
    woker = min(len(htmls_urls), MAX_WORKERS)
    with futures.ThreadPoolExecutor(woker) as executor:
        res = executor.map(get_img_url_one2, htmls_urls)
    return list(res)


def download_one(**kwargs):
    kw = kwargs
    print(kw)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54',
        'referer': kw['ref']
    }
    filename = kw['jpgurl'].split('/')[-1]
    resq = requests.get(kw['jpgurl'], headers=headers)
    return (resq.content, filename)


def download_one2(cc):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54',
        'referer': 'https://www.tooopen.com/view/2317533.html'
    }
    filename = cc.split('/')[-1]
    resq = requests.get(cc, headers=headers)
    save_img(resq.content,filename)
    show(url)
    return (resq.content, filename)


# 开始下载
def dowload_many(urls_list):
    filename_list = []
    for url in urls_list:
        content, filename = download_one(**url)
        ff = save_img(content, filename)
        show(url)
        filename_list.append(ff)
    return filename_list


def download_many_future(urls_list):
    worker = min(len(urls_list), MAX_WORKERS)
    with futures.ThreadPoolExecutor(worker) as executor:
        res = executor.map(download_one2, urls_list)
    return res


def save_img(context, filename):
    path = os.path.join(BASE_DIR, filename)
    with open(path, 'wb') as f:
        f.write(context)
    return filename


def show(text):
    print(text, end=' ')
    # print(text)
    sys.stdout.flush()


def main():
    URL = 'https://www.tooopen.com/img/88_878.aspx'
    htmls_urls = get_htmls(base_url=URL)
    jpg_list = get_img_urls(htmls_urls=htmls_urls)
    # print(jpg_list)
    ff = dowload_many(jpg_list)


def main_n(n):
    base_url = 'https://www.tooopen.com/img/88_878_1_{}.aspx'
    urls = []
    for i in range(1, n):
        url = base_url.format(i)
        htmls_urls = get_htmls(base_url=url)

        # jpg_list = get_img_urls(htmls_urls=htmls_urls)
        # print(jpg_list)
        p = get_img_future(htmls_urls=htmls_urls)
        urls += p
        print(urls)
        # # ff = download_many_future(jpg_list)
        # for i in jpg_list:
        #     ff = download_many_future(i)
    print(urls)
    ff = download_many_future(urls)


if __name__ == '__main__':
    main_n(30)
