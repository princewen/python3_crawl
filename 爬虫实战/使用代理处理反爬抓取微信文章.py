"""
作者：文文
内容：抓取微信文章
来源:崔庆才老师爬虫实战课程
版本: Python3.5
"""


"""
流程：
1、抓取索引页内容
2、代理设置：如果遇到302状态吗，则切换代理重试
3、分析详情页内容
4、将数据保存到数据库
"""

import requests
from urllib.parse import urlencode
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq

base_url = 'http://weixin.sogou.com/weixin?'
headers = {
    'Cookie':'IPLOC=CN1100; SUV=000250A26A78D57B58B5B94CF479A064; CXID=D2C8529E76DD4C4847DBADC4796433F7; ad=Tkllllllll2BljT5lllllV6laKkllllltfmHWyllllGlllllpOxlw@@@@@@@@@@@; SUID=7BD5786A2320940A0000000058B5B94C; ABTEST=1|1494401791|v1; SNUID=48F12D9D47420861C0B68A1C47B17FF0; weixinIndexVisited=1; sct=5; JSESSIONID=aaaRU64GLBEF45ApQ2UUv; ppinf=5|1494402094|1495611694|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTYlOTYlODclRTYlOTYlODd8Y3J0OjEwOjE0OTQ0MDIwOTR8cmVmbmljazoxODolRTYlOTYlODclRTYlOTYlODd8dXNlcmlkOjQ0Om85dDJsdUZ1RkpOdEVBME95SXIwcmhVQ1hGSk1Ad2VpeGluLnNvaHUuY29tfA; pprdig=SJUmasc9L-YCQeC0qovcfFXYwTWoan-c5RWbTC1nMrTBEvwM_Jku7YZ7tND3jjpWmAuWbtpKLaN-oYKTyEtcgdcovYfjHKuAhKJL3EciC7y8emTa-d8W4NzHW-fEnEZ44UJsNbbcgI-ugql_OUTb9Ls5LvHVq6Vl1E6Ib5bLU3I; sgid=; ppmdig=1494402094000000a6bb5960193b62bbd81844de31616416',
    'Host':'weixin.sogou.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}
keyword='风景'
proxy_pool_url = 'http://127.0.0.1:5000/get'
#全局代理
proxy = None
max_count = 5

def get_proxy():
    try:
        resposne = requests.get(proxy_pool_url)
        if resposne.status_code == 200:
            return resposne.text
        return None
    except ConnectionError:
        return None

def get_html(url,count = 1):
    print ('Crawling',url)
    print ('Trying Count',count)
    global proxy
    if count >= max_count:
        print ('Tried Too Many Counts')
        return None

    try:
        if proxy:
            proxies = {
                'http':'http://'+proxy
            }
        #加入allow_redirects才能拿到302信息
            response = requests.get(url,allow_redirects=False,headers=headers,proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            #Need Proxy
            print ('302')

            proxy = get_proxy()
            if proxy:

                print ('Using proxy',proxy)
                return get_html(url)
            else:
                print ('Get Proxy Failed')
                return None

    except ConnectionError as e:
        print ('Error Occureed',e.args)
        proxy = get_proxy()
        count+=1
        return get_html(url,count)


def get_index(keyword,page):
    data = {
        'query':keyword,
        'type':2,
        'page':page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html

def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')



def main():
    for page in range(1,101):
        html = get_index(keyword,page)
        #print (html)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                print (article_url)
                """解析article_url 无反爬机制，此处略"""
if __name__ == '__main__':
    main()

