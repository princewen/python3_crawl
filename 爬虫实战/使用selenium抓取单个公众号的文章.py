from selenium import webdriver
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import urllib.parse
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import DesiredCapabilities
import lxml.html
import pymongo
from lib.db_connection import *
import datetime
import time
from pymongo.errors import AutoReconnect

# url='https://mp.weixin.qq.com/profile?src=3&timestamp=1495698067&ver=1&signature=awlEuYd6RNvE29b8NZo7sKoi4aJjafIFA3f4Q5w3qPC8SHbbBUGmCiRdUGlQjMGiO8GrwRh*xt79OwBAH6iBCQ=='
caps = DesiredCapabilities.PHANTOMJS
caps["phantomjs.page.settings.userAgent"] = \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"

# driver = webdriver.PhantomJS(desired_capabilities=caps)
driver = webdriver.Chrome('/usr/local/Cellar/chrome/chromedriver', desired_capabilities=caps)
conn = pymongo.MongoClient('localhost',27017)
db = conn['news']


def get_text(elem):
    """提取一个元素的正文内容"""
    rc = []
    for node in elem.itertext():
        rc.append(node.strip())
    return ''.join(rc)


def get_one_page_content(href, times=0):
    """得到一片文章的正文，需要注意的是，要打开一个新的窗口再获取页面，最后要将页面关闭"""
    driver.execute_script('window.open()')

    driver.switch_to_window(driver.window_handles[1])
    driver.get(href)
    wait = WebDriverWait(driver, 10)
    # 首先判断是否是分享文章，如果是，得到连接，抓取来源处文章
    try:
        href = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="js_share_source"]'))).get_attribute(
            'href')
        driver.execute_script("window.close()")
        driver.switch_to_window(driver.window_handles[0])
        return get_one_page_content(href)
    # 如果不是分享文章，直接提取正文
    except:
        text = ''
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="js_content"]/p')))
            r = lxml.html.document_fromstring(driver.page_source)
            items = r.xpath('//*[@id="js_content"]/p')
            for item in items:
                itemtext = get_text(item).strip()
                if ((not itemtext.startswith('参考资料')) and (not itemtext.startswith('原文出处'))
                    and (not itemtext.startswith('本文系生物谷原创编译整理')) and (not itemtext.startswith('原始出处'))):
                    text += (itemtext + '\n')
            print(text)
        # 超时重抓
        except TimeoutException:
            print('超时，重新抓取')
            times += 1
            if times < 5:
                get_one_page_content(href, times)
            else:
                print('重新抓取次数超过限制，抓取失败')
        # 没有找到文章正文
        except NoSuchElementException:
            print('未找到文章内容，抓取失败')
        # 最后关闭文章窗口
        finally:
            driver.execute_script("window.close()")
            driver.switch_to_window(driver.window_handles[0])
            return text


def search_mongodb(url, times=0):
    """判断文章是否已经存在于mongodb中"""
    try:
        ret = db.weixin.find_one({'url': url})
        if not ret:
            return True
        else:
            return False
    except AutoReconnect:
        times += 1
        if times <= 5:
            print('连接错误，正在尝试重新连接mongodb')
            search_mongodb(url, times)
        else:
            print('mongodb连接失败')
            return False


def insert_mongodb(item, times=0):
    """文章插入mongodb中"""
    try:
        db.weixin.insert(item)
    except AutoReconnect:

        times += 1
        if times <= 5:
            print('连接错误，正在尝试重新连接mongodb')
            insert_mongodb(item, times)
        else:
            print('mongodb连接失败')


def search_mainpage(url, times=0):
    """函数入口，得到文章列表"""
    driver.get(url)

    # print (r.content)
    wait = WebDriverWait(driver, 10)
    try:
        items = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="history"]/div')))
        # items = dom.xpath('//*[@id="history"]/div')
        print(len(items))
        for item in items:
            subitems = item.find_elements_by_xpath('./div[2]/div')
            for subitem in subitems:
                href = 'https://mp.weixin.qq.com' + subitem.find_element_by_xpath('./div[1]/h4').get_attribute('hrefs')
                time = subitem.find_element_by_xpath('./div[1]/p[2]').text
                title = subitem.find_element_by_xpath('./div[1]/h4').text
                # 如果数据库中没有找到对应的文章，表明是一篇新文章，执行插入
                if search_mongodb(href):
                    content = get_one_page_content(href).strip()
                    spidertime = datetime.datetime.now().strftime('%b-%d-%y')
                    # 内容不为空则执行插入
                    if content != '':
                        insertitem = {'url': href, 'name': title, 'time': time, 'content': content,
                                      'spidertime': spidertime}
                        insert_mongodb(insertitem)

    # 超时处理，如果超过五次超时，则返回
    except TimeoutException:
        print('超时，重新抓取')
        times += 1
        if times < 5:
            search_mainpage(url, times)
        else:
            print('重新抓取次数超过限制，抓取失败')
            return ''
    # 找不到元素
    except NoSuchElementException:
        print('未找到相关文章，抓取失败')
        return ''


def search_sougou_page(query, times=0):
    base_url = 'http://weixin.sogou.com/weixin?'
    params = {
        'type': 1,
        'query': query
    }
    url = base_url + urllib.parse.urlencode(params)
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    try:
        href = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="sogou_vr_11002301_box_0"]/div/div[2]/p[1]/a'))).get_attribute('href')
        search_mainpage(href)
    # 超时处理，如果超过五次超时，则返回
    except TimeoutException:
        print('超时，重新抓取')
        times += 1
        if times < 5:
            search_sougou_page(query, times)
        else:
            print('重新抓取次数超过限制，抓取失败')
            return ''
    # 找不到元素
    except NoSuchElementException:
        print('未找到该公众号，抓取失败')
        return ''


if __name__ == '__main__':
    search_sougou_page('生物制药观察')

    driver.close()