#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from lxml import etree
import sys
import json
import asyncio
import aiohttp
import aiofiles
from io import BytesIO
from PIL import Image

# 定义架构

# 第一个页面，返回子页面url
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
}
base_dir = 'imgs'


async def get_html_girls(base_url):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(base_url, headers=headers) as response:
            urls_list = []
            result = await response.text()
            result = etree.HTML(result)
        parse_ul_list = result.xpath('//*[@id="container"]/ul/li')
        for urls in parse_ul_list:
            parse_li_list = urls.xpath('./div/a')
            for parse_div_list in parse_li_list:
                parse_a_list = parse_div_list.xpath('./@href')
                for i in parse_a_list:
                    if i.endswith('.html'):
                        urls_list.append(i)
        parse_script_list = result.xpath('//*[@id="data-more"]/text()')
        for p in parse_script_list:
            d = json.loads(p)
            for p in d:
                urls_list.append(p['url'])
    return urls_list


# 进入第二个页面

async def get_img_urls(url):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, headers=headers) as response:
            result = await response.text()
            result = etree.HTML(result)
        jpg = dict()
        img = result.xpath('//*[@id="imgView"]/@src')[0]
        jpg['img_url'] = str(img)
        jpg['ref_url'] = str(url)
    return jpg


# 进入img_url 返回content 和filename
async def get_img(img_url, ref_url):
    headers['referer'] = ref_url
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(img_url, headers=headers) as response:
            content = await response.read()
        imgs = dict()
        filename = img_url.split('/')[-1]
        imgs['filename'] = filename
        imgs['content'] = content
        path = os.path.join(base_dir,filename)
        # with open(path,'wb') as f:
        #     f.write(content)
        img = Image.open(BytesIO(content))
        img.save(path)
    return imgs


# 传入content，保存图片
async def save_img(filename, content):
    path = os.path.join(base_dir, filename)
    async with aiofiles.open(path, 'wb') as f:
        f.write(content)

def task_htmls_girls(base_url,n):
    return [get_html_girls(base_url=base_url.format(n)) for n in range(1,n) ]

def task_urls(htmls):
    task_list = []
    for i in htmls[0]:
        for j in i.result():
            task_list.append(get_img_urls(j))
    return task_list
def task_urls2(urls):
    task_list = []
    for i in urls[0]:
        task_list.append(get_img(**i.result()))
    return task_list

def task_imgs(imgs):
    task_list = []
    for i in imgs[0]:
        task_list.append(save_img(**i.result()))
    return task_list
# def task_save()

if __name__ == '__main__':
    base_url = 'https://www.tooopen.com/img/88_879_1_{}.aspx'
    tasks = task_htmls_girls(base_url,20)
    loop = asyncio.get_event_loop()
    htmls = loop.run_until_complete(asyncio.wait(tasks))
    tasks1 = task_urls(htmls)
    # tasks1 = [get_img_urls(html) for html in htmls]
    urls = loop.run_until_complete(asyncio.wait(tasks1))
    tasks2 = task_urls2(urls)
    imgs = loop.run_until_complete(asyncio.wait(tasks2))
    # tasks3 = task_imgs(imgs)
    # loop.run_until_complete(asyncio.gather(*tasks3))
    # img_task = []
    # for i in imgs[0]:
    #     print(i)
    # imgs_tasks = [get_img(img_url,ref_url) for img_url,ref_url in urls.values()]


