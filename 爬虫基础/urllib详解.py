
"""
作者：文文
内容：urllib库
来源:崔庆才老师爬虫实战课程
版本: Python3.5
"""

"""
urllib库

python内置的http请求库
四大模块：
urllib.request ：请求模块
urllib.error ： 异常处理模块
urllib.parse ：url解析模块
urllib.robotparser ：robots.txt 解析模块
"""

"""
相比python2变化
比如
python2中:
import urllib2
response = urllib2.urlopen('http://www.baidu.com')

python3中：
import urllib.request
response = urllib.request.urlopen('http://www.baidu.com')

"""

"""
urlopen函数
urlopen(url,data=None,[timeout,],other)
接受响应，响应中包含了状态码和响应头信息，使用read方法可以得到响应体的字节流（byte），再通过decode可以转换为utf8字符串
"""
import urllib.request

# get请求
response = urllib.request.urlopen("http://www.baidu.com")
# read方法返回的是byte格式的数据，需要decode成响应的编码格式
print (response.read().decode('utf-8'))

#post请求，加入data就以post方式发送请求
import urllib.parse
data=bytes(urllib.parse.urlencode({'word':'hello'}),encoding = "utf-8")
response = urllib.request.urlopen('http://httpbin.org/post',data=data)
print (response.read())

#timeout参数，如果在timeout设置的时间内没有返回请求，则会报错
response = urllib.request.urlopen('http://httpbin.org/get',timeout = 10)
print (response.read())

import socket
import urllib.error
try:
    response=urllib.request.urlopen('http://httpbin.org/get',timeout=0.1)
#进行异常处理，判断是否是超时错误
except urllib.error.URLError as e:
    if isinstance(e.reason,socket.timeout):
        print ("TIME OUT")



response = urllib.request.urlopen('http://python.org/')
#响应类型
print (type(response))
#状态码
print (response.status)
#响应头
print (response.getheaders())
print (response.getheader("Server"))
#read方法获得响应体，是byte类型的数据，需要decode得到utf8字符串
print (response.read().decode('utf-8'))

"""
Request 对象
"""
#使用Reqeust构造请求，与直接在urlopen方法中输入网址效果相同
request = urllib.request.Request('http://python.org')
response = urllib.request.urlopen(request)
print (response.read().decode('utf-8'))

#使用Request构造post请求
url='http://httpbin.org/post'
headers = {
    'User-Agent':'Mozilla/4.0(compatible;MSIE 5.5;Windows NT)',
    'Host':'httpbin.org'
}
dict ={
    'name':'Germey'
}
data=bytes(urllib.parse.urlencode(dict),encoding='utf-8')
request = urllib.request.Request(url=url,data=data,headers=headers,method='POST')
response=urllib.request.urlopen(request)
print (response.read().decode('utf-8'))


#add_header方法
url='http://httpbin.org/post'

dict ={
    'name':'Germey'
}
data=bytes(urllib.parse.urlencode(dict),encoding='utf-8')
request = urllib.request.Request(url=url,data=data,method='POST')
request.add_header('User-Agent','Mozilla/4.0(compatible;MSIE 5.5;Windows NT)')
response=urllib.request.urlopen(request)
print (response.read().decode('utf-8'))



"""
高级操作
Handler
"""

"""
代理ip  Handler
"""

proxy_handler = urllib.request.ProxyHandler({
    'http':'http://127.0.0.1:9743',
    'https':'http://127.0.0.1:9743'
})

opener = urllib.request.build_opener(proxy_handler)
response = opener.open('http://www.baidu.com')
print (response.read().decode('utf-8'))

"""
Cookie Handler
"""
# python利用cookiejar自动处理cookie
# 输出：
# BAIDUID=F6A6082952A8C27720B0EA23AED86E21:FG=1
# BIDUPSID=F6A6082952A8C27720B0EA23AED86E21
# H_PS_PSSID=1420_19035_21126_22748_22581
# PSTM=1493689482
# BDSVRTM=0
# BD_HOME=0
import http.cookiejar,urllib.request

cookie = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('http://www.baidu.com')
for item in cookie:
    print (item.name+'='+item.value)



#cookie保存到本地
filename = 'cookie.txt'
# 两种cookie保存方式
#cookie = http.cookiejar.LWPCookieJar(filename)
cookie = http.cookiejar.MozillaCookieJar(filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('http://www.baidu.com')
cookie.save(ignore_discard=True,ignore_expires=True)

#读取cookie
filename='cookie.txt'
cookie = http.cookiejar.LWPCookieJar()
cookie.load(filename,ignore_discard=True,ignore_expires=True)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('http://www.baidu.com')
print (response.read().decode('utf-8'))


"""异常处理模块
URlError 父类 只有reason属性
HTTPError 三个属性：code/reason/headers
"""


#请求页面不存在
#output : NOT Found
try:
    response = urllib.request.urlopen('http://cuiqingcai.com/index.htm')
except urllib.error.URLError as e:
    print (e.reason)

#捕捉异常

try:
    response = urllib.request.urlopen('http://cuiqingcai.com/index.htm')
except urllib.error.HTTPError as e :
    print (e.reason,e.code,e.headers,sep='\n')
except urllib.error.URLError as e:
    print (e.reason)

#捕捉超时请求异常
try:
    response=urllib.request.urlopen('http://httpbin.org/get',timeout=0.1)
#进行异常处理，判断是否是超时错误
except urllib.error.URLError as e:
    if isinstance(e.reason,socket.timeout):
        print ("TIME OUT")


"""URL解析
urlparse方法和urlunparse方法
urljoin方法和urlencode方法
"""

from urllib.parse import urlparse

#output : <class 'urllib.parse.ParseResult'>
# ParseResult(scheme='http', netloc='www.baidu.com', path='/index.html', params='user', query='id=5', fragment='comment')

result = urlparse('http://www.baidu.com/index.html;user?id=5#comment')
print (type(result),result)

#加入协议类型参数
result = urlparse('www.baidu.com/index.html;user?id=5#comment',scheme='https')
print (type(result),result)

#allow_fragments 是否允许锚点链接
#output : <class 'urllib.parse.ParseResult'>
# ParseResult(scheme='http', netloc='www.baidu.com', path='/index.html', params='user', query='id=5#comment', fragment='')

result = urlparse('http://www.baidu.com/index.html;user?id=5#comment',allow_fragments=False)
print (type(result),result)


#urlunparse 拼接url
from urllib.parse import urlunparse

#Output : http://www.baidu.com/index.html;user?a=6#comment
data =['http','www.baidu.com','index.html','user','a=6','comment']
print (urlunparse(data))

#urljoin 拼接url
# 以后面的url为基准

from urllib.parse import urljoin

# output : http://www.baidu.com/FAQ.html
print (urljoin('http://www.baidu.com','FAQ.html'))

# output : https://cuiqingcai.com/FAQ.html
print (urljoin('http://www.baidu.com','https://cuiqingcai.com/FAQ.html'))

# output : https://cuiqingcai.com/FAQ.html
print (urljoin('http://www.baidu.com/about.html','https://cuiqingcai.com/FAQ.html'))

# output : https://cuiqingcai.com/FAQ.html?question=2
print (urljoin('http://www.baidu.com/about.html','https://cuiqingcai.com/FAQ.html?question=2'))

# output : https://cuiqingcai.com/index.php
print (urljoin('http://www.baidu.com?wd=abc','https://cuiqingcai.com/index.php'))

# output : http://www.baidu.com?category=2#comment
print (urljoin('http://www.baidu.com','?category=2#comment'))

# output : www.baidu.com?category=2#comment
print (urljoin('www.baidu.com','?category=2#comment'))

# output : www.baidu.com?category=2
print (urljoin('www.baidu.com#comment','?category=2'))

#urlencode 将字典转换为请求参数
from urllib.parse import urlencode

params = {
    'name' : 'germey',
    'age':22
}
base_url = 'http://www.baidu.com?'

url = base_url + urlencode(params)
#output : http://www.baidu.com?age=22&name=germey
print (url)










