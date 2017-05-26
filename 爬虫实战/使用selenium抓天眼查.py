"""
使用selenium爬取天眼查六个板块的信息
地区  行业  规模  股东类型 专利数  成立时间
"""
from selenium import webdriver
import time
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import urllib
from selenium.common.exceptions import TimeoutException
import pymysql
import re





"""搜索起始页，得到详情页的网址"""
def search_mainpage(query,times=0):
    try:
        baseurl = 'http://www.tianyancha.com/search?'
        params = {
            'key':query,
            'checkForm':'searchBox'
        }
        url = baseurl + urllib.parse.urlencode(params)
        print (url)
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        try:
            href = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ng-view"]/div[2]/div/div/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/a'))).get_attribute('href')
        except Exception as e:
            print ('未找到该结果')
            href = ''
        return href

    except TimeoutException:
        print ('crawl again')
        if times < 5:
            times+=1
            search_mainpage(query,times)
        else:
            return ''


"""对money字符串进行处理
输入：页面中的字符串，如(人民币)6500万元
输出：[类型，金额，单位] ，如['人民币', '6500.0000', '万']
"""
def parse_money(money):
    pattern1 = re.compile(r'(\(人民币|美元\))([\d.]+)(.*?)')
    pattern2 = re.compile(r'([\d.]+)(.*?)(人民币|美元)')
    match1 = pattern1.search(money)
    match2 = pattern2.search(money)
    if match1:
        return [match1.group(1)[1:-1],match1.group(2),match1.group(3)]
    elif match2:
        return [ match2.group(3),match2.group(1), match2.group(2)]
    else:
        return [0,0,0]

"""搜索详情页
输入：公司详细内容的网址
输出：公司地区  行业  规模  股东类型 专利数  成立时间的信息
"""
def search_detail(href,times=0):
    try:
        driver.get(href)
        wait = WebDriverWait(driver, 10)
        # 公司名称
        try :
            company_name = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ng-view"]/div[2]/div/div/div/div[1]/div[1]/div[2]/div/span'))).text
        except Exception as e:
            company_name = ''
        # 公司地址
        try:
            location = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ng-view"]/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div[3]/div[2]/span[2]'))).text
        except Exception as e:
            location = ''
        # 公司行业
        try:
            industry = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ng-view"]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[3]/table/tbody/tr[3]/td[1]/div/span'))).text
        except Exception as e:
            industry = ''
        # 公司注册资本
        try:
            money = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ng-view"]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/table/tbody/tr/td[2]/div'))).text
            #money = parse_money(money)
        except Exception as e:
            #money = ['','','']
            money = ''
        # 股东列表
        try:
            holders_element = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="ng-view"]/div[2]/div/div/div/div[2]/div/div[2]/div[5]/div[2]/table/tbody/tr')))
            holders = []
            for element in holders_element:
                holder = element.find_element_by_xpath('./td[1]/a').text
                #print (holder)
                holders.append(holder)
        except Exception as e:
            holders=[]

        # 成立时间
        try:
            build_time = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ng-view"]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/table/tbody/tr/td[3]/div'))).text
        except Exception as e:
            build_time = ''

        # 专利数量
        try:
            patent_count = driver.find_element_by_id('nav-main-patentCount').find_element_by_xpath('./span').text.strip()[1:-1]
        except Exception as e:
            #print (e.args)
            patent_count = 0

        # 著作权
        try:
            copyright_count = driver.find_element_by_id('nav-main-cpoyRCount').find_element_by_xpath('./span').text.strip()[1:-1]
        except Exception as e:
            #print (e.args)
            copyright_count = 0
        print (company_name,location,industry,money,build_time,holders,patent_count,copyright_count)

    except TimeoutException as e:
        print (e.args)

        if times < 5:
            print('crawl again')
            times += 1
            search_detail(href,times)
        else:
            return []


if __name__ == '__main__':
    try:
        driver = webdriver.Chrome('/usr/local/Cellar/chrome/chromedriver')
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(20)
        conn = pymysql.Connect(host='106.75.65.56',port=3306,user='root',passwd='wotou',db='news',charset='utf8')
        cur = conn.cursor()
        cur.execute('select name from stopcompanys limit 500')
        results= cur.fetchall()
        for company in results:
            print ('crawing : {}'.format(company[0]))
            href = search_mainpage(company[0])
            if href != '':
                search_detail(href)
            time.sleep(3)
    except Exception as e:
        print (e.args)

    finally:
        conn.close()
        driver.close()

