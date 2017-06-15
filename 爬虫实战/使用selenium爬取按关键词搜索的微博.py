from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import DesiredCapabilities
import selenium.webdriver.support.expected_conditions as EC
import lxml.html
import pymongo
import re
import time

caps = DesiredCapabilities.PHANTOMJS
caps["phantomjs.page.settings.userAgent"] = \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"

driver = webdriver.Chrome('/usr/local/Cellar/chrome/chromedriver', desired_capabilities=caps)
start_url = 'http://weibo.com'

user = '18810983661'
passwd = 'wasjwj306'

query = '休斯顿火箭'

page = 3

def get_text(elem):
    """提取一个元素的正文内容"""
    rc = []
    for node in elem.itertext():
        rc.append(node.strip())
    return ''.join(rc)


def save_to_mongodb():
    """将数据保存到mongodb中"""
    pass

def parse_per_page():
    """解析每一页的内容"""
    wait = WebDriverWait(driver, 10)
    weibos_wrap = driver.find_elements_by_xpath('//div[@class="WB_cardwrap S_bg2 clearfix"]')
    """点击每个展开全文"""
    for per_weibo in weibos_wrap:
        try:
            whole = per_weibo.find_element_by_xpath('.//i[@class="W_ficon ficon_arrow_down"]')
            print('展开全文')
            whole.click()
            wait.until(EC.presence_of_element_located((By.XPATH,'.//p[@class="comment_txt"][2]')))
        except Exception as e:
            print (e.args)
            print ('无展开全文')

    time.sleep(10)
    """使用lxml解析页面内容"""
    dom = lxml.html.document_fromstring(driver.page_source)
    weibos_wrap = dom.xpath('//div[@class="WB_cardwrap S_bg2 clearfix"]')

    for per_weibo in weibos_wrap:
        pattern = re.compile('<.*?>|</.*?>')
        weibo_user = per_weibo.xpath('./div/div[1]/dl/div/div[3]/div[1]/a[1]')[0].text
        print (len(per_weibo.xpath('.//p[@class="comment_txt"]')))
        if len(per_weibo.xpath('.//p[@class="comment_txt"]'))>1:
            weibo_content = get_text(per_weibo.xpath('.//p[@class="comment_txt"]')[1])
        else:
            weibo_content = get_text(per_weibo.xpath('.//p[@class="comment_txt"][1]')[0])
        weibo_content = re.sub(pattern, '', weibo_content)
        print (weibo_user,weibo_content)

    # weibos_wrap = driver.find_elements_by_xpath('//div[@class="WB_cardwrap S_bg2 clearfix"]')
    # for per_weibo in weibos_wrap:
    #     try:
    #         whole = per_weibo.find_element_by_xpath('.//a[@class="WB_text_opt"]')
    #         print('展开全文')
    #         whole.click()
    #
    #     except:
    #         print ('无展开全文')
    #
    # weibos_wrap = driver.find_elements_by_xpath('//div[@class="WB_cardwrap S_bg2 clearfix"]')
    # pattern = re.compile('<.*?>|</.*?>')
    # for per_weibo in weibos_wrap:
    #     weibo_user = per_weibo.find_element_by_xpath('./div/div[1]/dl/div/div[3]/div[1]/a[1]').text
    #     weibo_content = per_weibo.find_element_by_xpath('.//p[@class="comment_txt"][1]').text
    #
    #     weibo_content = re.sub(pattern,'',weibo_content)
    #     print (weibo_user,weibo_content)

def search(query,page):
    """按关键词搜索微博"""
    basic_url = 'http://s.weibo.com/weibo/'+query+'?topnav=1&wvr=6&b=1&page='
    for i in range(1,page+1):
        driver.get(basic_url+str(i))
        parse_per_page()


def login():
    """模拟登陆微博,不登陆貌似只能看一页"""
    driver.get(start_url)
    wait = WebDriverWait(driver,10)
    try:
        username = wait.until(EC.presence_of_element_located((By.ID,"loginname")))
        password = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input')))
        username.send_keys(user)
        password.send_keys(passwd)
        btn = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pl_login_form"]/div/div[3]/div[6]/a/span')))
        btn.click()
    except TimeoutException:
        print ("超时")
        return
    except NoSuchElementException:
        print ("找不到该元素 ")
        return

def main():
    #login()
    search(query,page)
    driver.close()



if __name__ == '__main__':
    main()