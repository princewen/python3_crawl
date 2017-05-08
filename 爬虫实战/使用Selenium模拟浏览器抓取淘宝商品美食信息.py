"""
作者：文文
内容：使用selenium抓取淘宝美食
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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from pyquery import PyQuery as pq


#browser = webdriver.Chrome('/usr/local/Cellar/chrome/chromedriver')
browser = webdriver.PhantomJS()
wait = WebDriverWait(browser,20)

"""起始页，在搜索框中输入美食并跳转"""
def search():
    try :
        browser.get('https://www.taobao.com')
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#q')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
        input.send_keys('美食')
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        return total.text
    except TimeoutException:
        return search()

"""进行翻页，得到下一页的内容"""
def next_page(page_number):
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > input')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        get_products()
    except TimeoutException:
        return next_page(page_number)

"""
获取到每一页的商品信息
使用pyquery进行解析
"""
def get_products():
    wait.until(EC.presence_of_element_located((By.ID,'mainsrp-itemlist')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image' : item.find('.pic .img').attr('src'),
            'price' : item.find('.price').text(),
            'deal' : item.find('deal-cnt').text()[:-3],
            'title' : item.find('.title').text(),
            'shop' : item.find('.shop').text(),
            'location' : item.find('.location').text()
        }
        print (product)



"""主程序入口"""
def main():
    try:
        total = search()
        total = int (re.compile('(\d+)').search(total).group(1))
        print (total)
        for i in range(2,total+1):
            next_page(i)
    except Exception:
        print ('出错啦')
    finally:
        browser.close()


if __name__ == '__main__':
    main()