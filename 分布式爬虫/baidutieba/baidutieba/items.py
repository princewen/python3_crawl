# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaidutiebaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author_id = scrapy.Field()
    author_name = scrapy.Field()
    stairs = scrapy.Field()
    comments = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()

