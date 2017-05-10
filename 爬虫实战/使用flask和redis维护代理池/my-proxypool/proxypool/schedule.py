from multiprocessing import Process
from proxypool.setting import *
from proxypool.db import RedisClient
from proxypool.getter import FreeProxyGetter
from proxypool.error import ResourceDepletionError
import time
import aiohttp
import asyncio
try:
    from aiohttp.errors import ProxyConnectionError
except:
    from aiohttp import  ClientProxyConnectionError as ProxyConnectionError

class ValidityTester(object):
    test_api = TEST_API

    def __init__(self):
        self._raw_proxies = None
        self._usable_proxies = []

    def set_raw_proxies(self,proxies):
        self._raw_proxies = proxies
        self._conn = RedisClient()

    async def test_single_proxy(self,proxy):
        """
                text one proxy, if valid, put them to usable_proxies.
        """
        async with aiohttp.ClientSession() as session:
            try:
                if isinstance(proxy,bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://'+proxy
                print ('Testing ' + real_proxy)
                #  使用百度进行测试，如果能够访问，则说明代理ip可以用
                async with session.get(self.test_api,proxy=real_proxy,timeout=15) as response:
                    if response.status == 200:
                        self._conn.put(proxy)
                        print ('Vaild proxy',proxy)
            except (ProxyConnectionError,TimeoutError,ValueError):
                print ('Invaild proxy',proxy)

    def test(self):
        """
                aio test all proxies.
        """
        try:
            loop = asyncio.get_event_loop()
            tasks = [self.test_single_proxy(proxy) for proxy in self._raw_proxies]
            loop.run_until_complete(asyncio.wait(tasks))
        except ValueError:
            print ('asyncio error')

class PoolAdder(object):
    """
        add proxy to pool
    """
    def __init__(self,threhold):
        self.threhold = threhold
        self._conn = RedisClient()
        self._tester = ValidityTester()
        self._crawler = FreeProxyGetter()

    def is_over_threhold(self):
        """
                judge if count is overflow.
        """
        if self._conn.queue_len > self.threhold:
            return True
        else:
            return False

    def add_to_queue(self):
        print('PoolAdder is working')
        proxy_count = 0
        while not self.is_over_threhold():
            for callback_label in range(self._crawler.__CrawlFuncCount__):
                callback = self._crawler.__CrawlFunc__[callback_label]
                raw_proxies = self._crawler.get_raw_proxies(callback)
                # test crawled proxies
                self._tester.set_raw_proxies(raw_proxies)
                self._tester.test()
                proxy_count+=len(raw_proxies)
                if self.is_over_threhold():
                    print('IP is enough, waiting to be used')
                    break
            if proxy_count == 0:
                raise ResourceDepletionError







class Schedule(object):

    """在不需要类实例化的时候就可以调用"""
    @staticmethod
    def vaild_proxy(cycle=VALID_CHECK_CYCLE):
        """Get half of proxies which in redis"""
        conn = RedisClient()
        tester = ValidityTester()
        while True:
            print ('refresing ip')
            count = int(0.5 * conn.queue_len)
            if count == 0:
                print('Waiting for adding')
                time.sleep(cycle)
                continue
            raw_proxies = conn.get(count)
            tester.set_raw_proxies(raw_proxies)
            tester.test()
            time.sleep(cycle)


    @staticmethod
    def check_pool(lower_threhold=POOL_LOWER_THRESHOLD,
                   upper_threhold=POOL_UPPER_THRESHOLD,
                   cycle=POOL_LEN_CHECK_CYCLE):
        """
                If the number of proxies less than lower_threshold, add proxy
        """
        conn = RedisClient()
        adder = PoolAdder(upper_threhold)
        while True:
            if conn.queue_len < lower_threhold:
                adder.add_to_queue()
            time.sleep(cycle)


    def run(self):
        print ('IP processing running')
        vaild_process = Process(target=Schedule.vaild_proxy)
        check_process = Process(target=Schedule.check_pool)
        vaild_process.start()
        check_process.start()


