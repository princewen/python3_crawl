
"""
作者：文文
内容：selenium
来源:崔庆才老师爬虫实战课程
版本: Python3.5
"""

"""selenium:自动化测试工具，支持多种浏览器
主要用来解决JavaScript渲染的问题
安装:pip install selenium
"""

"""基本使用"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()
try:
    browser.get('https://www.baidu.com')
    #找到百度的输入框
    input = browser.find_element_by_id('kw')
    #在输入框中输入python
    input.send_keys('Python')
    #回车进行搜索
    input.send_keys(Keys.ENTER)
    #等待10s
    wait  = WebDriverWait(browser,10)
    #直到contnet_left元素出现
    wait.until(EC.presence_of_element_located((By.ID,'content_left')))
    #打印当前url
    print (browser.current_url)
    #打印当前的cookie
    print (browser.get_cookies())
    #打印当前的源代码
    print (browser.page_source)
finally:
    browser.close()

"""声明浏览器对象"""
from selenium import webdriver

#browser = webdriver.Chrome()
browser= webdriver.PhantomJS()

"""访问页面"""
browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
print (browser.page_source)
browser.close()

"""查找元素"""

#单个元素
#除了下面的方式外，还有其它方式
browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input_first = browser.find_element_by_id('q')
input_second = browser.find_element_by_css_selector('#q')
input_third = browser.find_element_by_xpath('//*[@id="q"]')
print (input_first,input_second,input_third)
browser.close()

#通用方式
browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input_first = browser.find_element(By.Id,'q')
print (input_first)
browser.close()


#查找多个元素
browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
lis = browser.find_elements_by_css_selector(('.service-bd li'))
lis_2 = browser.find_elements(By.CSS_SELECTOR,'.service-bd li')
#返回一个列表
print (lis)
print (lis_2)
browser.close()


"""元素交互操作"""

import time

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input = browser.find_element_by_id('q')
input.send_keys('iPhone')
time.sleep(1)
input.clear()
input.send_keys('iPad')
button = browser.find_element_by_class_name('btn-search')
button.click()


"""交互动作
将动作附加到动作链中串行执行
"""

from selenium.webdriver import ActionChains
browser = webdriver.Chrome()
url = 'http://www.runoob.com/try/try.php?filename=jqueryul-api=dropable'
browser.get(url)
#切换到iframe
browser.switch_to.frame('iframeResult')
source = browser.find_element_by_css_selector('#draggable')
target = browser.find_element_by_css_selector('#droppable')

actions = ActionChains(browser)
actions.drag_and_drop(source,target)
actions.perform()

"""执行javascript"""
browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
browser.execute_script('alert("To Bottom")')
browser.close()

"""获取元素属性"""

browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
logo = browser.find_element_by_id('zh-top-link-logo')
print (logo)
# 获取class
print (logo.get_attribute('class'))

input = browser.find_element_by_class_name('zu-top-add-question')
#获取文本
print (input.text)
#获取其他信息
print (input.id)
print (input.location)
print (input.tag_name)
print (input.size)


"""frame
不能在子frame中查找父frame的内容
"""

from selenium.common.exceptions import NoSuchElementException
browser = webdriver.Chrome()
url = 'http://www.runoob.com/try/try.php?filename=jqueryul-api=dropable'
browser.get(url)
#切换到iframe
browser.switch_to.frame('iframeResult')
source = browser.find_element_by_css_selector('#draggable')
try:
    logo = browser.find_element_by_class_name('logo')
except NoSuchElementException:
    print ('NO LOGO')

browser.switch_to.parent_frame()
logo = browser.find_element_by_class_name('logo')
print (logo)
print (logo.text)


"""等待"""


browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
"""隐式等待"""
browser.implicitly_wait(10)
"""如果这个元素没有找到的话，会等待10s，如果还没有找到，就会抛出异常"""
logo = browser.find_element_by_id('zh-top-link-logo')
print (logo)
# 获取class
print (logo.get_attribute('class'))
browser.close()


"""显示等待"""

browser = webdriver.Chrome()
browser.get('https://www.taobao.com/')
wait = WebDriverWait(browser,10)
#参数是元组，还有其他一些等待条件
input = wait.until(EC.presence_of_element_located((By.ID,'q')))
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.btn-search')))
browser.close()

"""前进后退"""
browser = webdriver.Chrome()
browser.get('https://www.baidu.com')
browser.get('https://www.taobao.com')
browser.get('https://www.python.org')
browser.back()
time.sleep(1)
browser.forward()
browser.close()


"""Cookies"""

browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
print (browser.get_cookies())
browser.add_cookie({'name':'name','domain':'www.zhihu.com','value':'germey'})
print (browser.get_cookies())
browser.delete_all_cookies()
print (browser.get_cookies())



"""选项卡管理"""

browser = webdriver.Chrome()
browser.get('https://www.baidu.com')
browser.execute_script('window.open()')
print (browser.window_handles)
browser.switch_to_window(browser.window_handles[1])
browser.get('https://www.zhihu.com/explore')
browser.switch_to_window(browser.window_handles[0])
browser.get('https://python.org')
browser.close()


"""异常处理"""
from selenium.common.exceptions import NoSuchElementException,TimeoutException
browser = webdriver.Chrome()
try:
    browser.get('https://www.baidu.com')
except TimeoutException:
    print ('TIme out')

try:
    browser.find_element_by_id('hello')
except NoSuchElementException:
    print ('NOT FOUND')









