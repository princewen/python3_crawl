
"""
作者：文文
内容：urllib库
来源:崔庆才老师爬虫实战课程
版本: Python3.5
"""

"""

Requests 基于 urllib，简单易用的http库
安装：pip install requests

"""

"""实例引入"""

import requests

response = requests.get('http://www.baidu.com')
print (type(response))
print (response.status_code)
#<class 'str'>,不需要转码
print (type(response.text))
print (response.text)
print (response.cookies)

"""请求方式"""

post_res = requests.post("http://httpbin.org/post")
put_res = requests.put('http://httpbin.org/put')
delete_res = requests.delete('http://httpbin.org/delete')
head_res = requests.head('http://httpbin.org/get')
options_res = requests.options('http://httpbin.org/get')

"""基本GET请求"""

#基本
response = requests.get('http://httpbin.org/get')
print (response.text)

#带参数的GET请求
response = requests.get('http://httpbin.org/get?name=germy&age=22')
print (response.text)

data = {
    'name':'geremy',
    'age':22
}
response = requests.get('http://httpbin.org/get',params = data)
print (response.text)


#解析json
import json

response = requests.get('http://httpbin.org/get')
print (type(response.text))
#相当于调用了json.loads()
print (response.json())
print (json.loads(response.text))
print (type(response.json()))

#获取二进制数据
response = requests.get('http://github.com/favicon.ico')
with open('favicon.ico','wb') as f:
    f.write(response.content)
    f.close()


#添加headers
#不加headers爬取知乎直接报错500
response = requests.get('https://wwww.zhihu.com/explore')
print (response.text)

#添加可以正确返回
headers = {
    'User-Agent':'Mozilla/4.0(compatible;MSIE 5.5;Windows NT)',
}
response = requests.get('https://www.zhihu.com/explore',headers = headers)
print (response.text)


"""基本POST请求"""

data = {
    'name':'germey',
    'age':22
}
response = requests.post('http://httpbin.org/post',data = data)
print (response.text)


"""响应 response属性"""

response = requests.get('http://www.jianshu.com')
#状态码
print (type(response.status_code),response.status_code)
#请求头
print (type(response.headers),response.headers)
print (type(response.cookies),response.cookies)
#请求的url
print (type(response.url),response.url)
#历史记录
print (type(response.history),response.history)

"""高级操作"""

#文件上传
files = {'file':open('favicon.ico','rb')}
response = requests.post('http://httpbin.org/post',files=files)
print (response.text)

#获取cookie
response=requests.get('https://www.baidu.com')
print (response.cookies)
for key,value in response.cookies.items():
    print (key+'='+value)

#会话维持
s = requests.Session()
s.get('http://httpbin.org/cookies/set/number/123456789')
response = s.get('http://httpbin/org/cookies')
print (response.text)

#证书验证
#请求https网站时，首先判断证书是不是合法的，即ssl协议
# 想要避免证书验证，设置verify参数设置为False，比如12306，但是这样会被警告
from requests.packages import urllib3
#消除警告
urllib3.disable_warnings()
response = requests.get('https://www.12306.com',verify=False)
print (response.status_code)


#也可以手动指定CA证书
response = requests.get('https://www.12306.com',cert=('/path/server.crt','path/key'))
print (response.text)

#代理设置
proxy = {
    'http':'http://127.0.0.1:9743',
    'https':'http://127.0.0.1:9743'
}
response = requests.get('https://www.taobao.com',proxies=proxy)
print (response.status_code)

#使用socks代理
#需要先安装相应模块 pip install 'reqeusts[socks]'
proxy = {
    'http':'socks5://127.0.0.1:9742',
    'https':'socks5://127.0.0.1:9742'
}
response = requests.get('https://www.taobao.com',proxy=proxy)
print (response.status_code)

#超时设置
from requests.exceptions import  ReadTimeout
try:
    response = requests.get('http://www.taobao.com',timeout=1)
    print (response.status_code)
except ReadTimeout:
    print ('TImeout')

#认证设置
from requests.auth import HTTPBasicAuth

#response = requests.get('http://127.27.34.24:9001',auth=('user','123'))
response = requests.get('http://127.27.34.24:9001',auth=HTTPBasicAuth('user','123'))
print (response.status_code)

# 异常处理
import requests
from requests.exceptions import ReadTimeout,HTTPError,RequestException
try:
    response = requests.get('http://httpbin.org/get',timeout=0.5)
    print (response.status_code)
except ReadTimeout:
    print ('Timeout')

except HTTPError:
    print ('Http error')

except RequestException:
    print ('Error')

