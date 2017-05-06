"""
作者：文文
内容：今日头条街拍
来源:崔庆才老师爬虫实战课程
版本: Python3.5
"""


"""
流程：
1、抓取索引页内容
2、抓取详情页内容
3、下载图片与保存数据库
4、开启循环及多进程
"""

import requests
from urllib.parse import urlencode
from requests.exceptions import RequestException
import json
from bs4 import BeautifulSoup
import re
import pymongo
import os
from hashlib import md5
from multiprocessing import Pool
from json import JSONDecodeError

"""mongodb配置"""
client = pymongo.MongoClient('localhost')
db = client['crawler']

"""获取首页的内容"""
def get_page_index(offset,keyword):
    data = {
        'offset':offset,
        'format':'json',
        'keyword':keyword,
        'autoload':'true',
        'count':'20',
        'cur_tab':3
    }
    url = 'http://www.toutiao.com/search_content?'+urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print ("请求索引出错")
        return None

"""解析首页内容"""
def parse_page_index(html):
    try:
        data = json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass

"""得到详情页内容"""
def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code==200:
            return response.text
        return None

    except RequestException:
        print ('请求详情页出错',url)
        return None


"""解析详情页内容"""
def parse_page_detail(html,url):
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('title')[0].get_text()
    images_pattern = re.compile('var gallery = (.*?);',re.S)
    result = re.search(images_pattern,html)
    if result:
        data = json.loads(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:
                download_image(image)
            return {
                'title':title,
                'url':url,
                'images':images
            }

"""将页面保存到mongodb"""
def save_to_mongo(result):
    #print (result)
    if result and db['toutiao'].insert(result):
        print ('存储到mongodb成功',result)
        return True
    return False

"""下载图片内容"""
def download_image(url):
    try:
        response = requests.get(url)
        print ('正在下载：',url)
        if response.status_code==200:
            #content是二进制内容
            save_image(response.content)
        return None

    except RequestException:
        print ('请求图片出错',url)
        return None

"""保存图片"""
def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()

"""主函数入口"""
def main(offset):
    html=get_page_index(offset,'街拍')

    for url in parse_page_index(html):
        print (url)
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html,url)
            save_to_mongo(result)


if __name__ == '__main__':
    main()
    groups = [x*20 for x in range(1,20)]
    pool = Pool()
    pool.map(main,groups)


