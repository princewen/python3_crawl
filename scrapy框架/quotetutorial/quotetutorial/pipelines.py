# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo

class TextPipeline(object):

    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0:self.limit]
            return item
        else:
            return DropItem('Missing Text')

class MongoPipeline(object):

    def __init__(self,monog_uri,mongo_db):
        self.mongo_uri = monog_uri
        self.mongo_db = mongo_db

    #从setting拿到一些配置信息
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            monog_uri=crawler.settings.get('Mongo_uri'),
            monog_db = crawler.settings.get('monog_db')
        )


    def open_spider(self):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self,item,spider):
        self.db['quotes'].insert(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()