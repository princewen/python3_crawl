"""
作者：文文
内容：猫眼电影top100
来源:崔庆才老师爬虫实战课程
版本: Python3.5
"""

"""
流程：
1、抓取单页内容
2、正则表达式分析
3、保存到文件
4、循环抓取100个表单
"""

import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

"""得到每一页的页面内容"""
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

"""使用正则表达式解析网页"""
def parse_one_page(html):
    pattern = re.compile(r'<dd>.*?board-index-.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>',re.S)
    #print (html)
    items = re.findall(pattern,html)
    #print (items)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4].strip()[5:],
            'score':item[5]+item[6]
        }

"""按照json格式写入文件"""
def write_to_file(content):
    with open('result.txt','a') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()

"""主函数"""
def main(offset):
    url = "http://maoyan.com/board/4?offset="+str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print (item)
        write_to_file(item)

"""使用进程池进行爬取"""
if __name__ == '__main__':

    pool=Pool()
    pool.map(main,[i*10 for i in range(10)])

