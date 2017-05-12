# -*- coding: utf-8 -*-
import scrapy
from quotetutorial.items import QuotetutorialItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    #默认的回调函数
    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')
        print (len(quotes))
        for quote in quotes:
            item = QuotetutorialItem()
            text = quote.xpath('./span[@class="text"]/text()').extract_first()
            author = quote.xpath('./span[2]/small/text()').extract_first()
            tags = quote.xpath('./div[@class="tags"]/a/text()').extract()
            #print (text,author,tags)
            item['text']=text
            item['author']=author
            item['tags'] = tags
            yield item

        next = response.xpath('//li[@class="next"]/a/@href').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url,callback=self.parse)
        #scrapy crawl quotes -o test.json 保存到json文件
        #scrapy crawl quotes -o test.csv
