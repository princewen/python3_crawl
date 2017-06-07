# -*- coding: utf-8 -*-
import scrapy
import json
from collections import defaultdict
import urllib.parse
from baidutieba.items import BaidutiebaItem
import re

class TiebaSpider(scrapy.Spider):
    name = 'tieba'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['https://tieba.baidu.com/f?kw=%E8%81%8A%E5%A4%A9&ie=utf-8&pn=0']
    base_url = 'https://tieba.baidu.com'


    def parse(self, response):
        lis = response.xpath('//*[@id="thread_list"]/li[@class=" j_thread_list clearfix"]')
        for li in lis:
            try:
                item = BaidutiebaItem()
                author_id = li.xpath('./div/div[2]/div[1]/div[2]/span[1]/@data-field')[0].extract()
                item['author_id'] = json.loads(author_id)['user_id']
                author_nickname = li.xpath('./div/div[2]/div[1]/div[2]/span[1]/span[1]/a/text()').extract_first()
                item['author_name'] = author_nickname
                item['title'] = li.xpath('./div/div[2]/div[1]/div[1]/a/text()').extract_first()
                item['url'] = self.base_url + li.xpath('./div/div[2]/div[1]/div[1]/a/@href').extract_first()

                #print (author_id,author_nickname,tiezi_title,tiezi_url)
                yield scrapy.Request(item['url'],callback=self.parse_content,meta = {'item':item})
                for i in range(1,6):
                    url = 'https://tieba.baidu.com/f?kw=%E8%81%8A%E5%A4%A9&ie=utf-8&pn='+str(i*50)
                    yield scrapy.Request(url,callback=self.parse)
            except:
                continue


    def parse_content(self,response):
        item = response.meta['item']
        item['stairs'] = dict()
        stairs = response.xpath('//*[@id="j_p_postlist"]/div[@class="l_post l_post_bright j_l_post clearfix  "]')
        #print (len(stairs))
        for index,stair in enumerate(stairs):
            item['stairs'][str(index)] = {}
            item['stairs'][str(index)]['comment_id'] = json.loads(stair.xpath('./@data-field').extract_first())['content']['post_id']
            item['stairs'][str(index)]['content'] = stair.xpath('./div[2]/div[1]/cc/div[1]/text()').extract_first().strip()
            item['stairs'][str(index)]['stair_user_id'] = json.loads(stair.xpath('./div[1]/ul/li[3]/@data-field').extract_first())['user_id']
            item['stairs'][str(index)]['stair_user_name'] = stair.xpath('./div[1]/ul/li[3]/a/text()').extract_first()

            try:
                if index == 0 :
                    item['stairs'][str(index)]['index'] = stair.xpath('./div[2]/div[4]/div[1]/div/span[3]/text()').extract_first()
                    item['stairs'][str(index)]['time'] = stair.xpath('./div[2]/div[4]/div[1]/div/span[4]/text()').extract_first()
                else:
                    item['stairs'][str(index)]['index'] =  stair.xpath('./div[2]/div[2]/div[1]/div[2]/span[3]/text()').extract_first()
                    item['stairs'][str(index)]['time'] =  stair.xpath('./div[2]/div[2]/div[1]/div[2]/span[4]/text()').extract_first()

            except Exception as e:
                print (e.args)
                continue

        params = {
            'fid':9532,
            'pn':1
        }
        params['tid']=response.url.split('/')[-1]
        url = 'https://tieba.baidu.com/p/totalComment?'+ urllib.parse.urlencode(params)
        yield scrapy.Request(url,callback = self.parse_comment,meta = {'item':item})

    def parse_comment(self,response):
        item = response.meta['item']
        item['comments'] = json.loads(response.text)
        #print (item['comments'])
        yield item








