# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging



class HttpbintestSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):

    logger = logging.getLogger(__name__)

    def process_request(self,request,spider):
        self.logger.debug('Using proxy')
        #设置代理
        request.meta['proxy'] = 'http://127.0.0.1:9743'
        #如果返回None，继续处理request，执行完所有中间件的process_request
        # 如果返回request，则会加入新的执行队列
        # 如果返回response，则不会调用process_request,直接调用其他中间件的process_response
        return None

    def process_response(self,request,response,spider):
        # 返回response，继续执行其他中间件的process_response
        # 返回request，将request加入调度队列
        # 返回exception，进行异常处理
        response.status = 201
        return response



    def process_exception(self,request,exception,spider):
        # 返回None,不影响其他操作，继续执行其他的process_request
        # 如果返回response，则继续执行其他的process_response
        # 如果返回request，重新将reqeust加入调度队列，重新请求
        self.logger.debug('Get Exception')
        self.logger.debug('Try second Time')
        request.meta['proxy'] = 'http://127.0.0.1:9743'
        return request




