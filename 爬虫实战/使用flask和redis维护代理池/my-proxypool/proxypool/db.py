import redis
from proxypool.error import PoolEmptyError
from proxypool.setting import HOST, PORT, PASSWORD


#redis队列相关操作
class RedisClient(object):
    def __init__(self,host=HOST,port=PORT):
        if PASSWORD:
            self._db = redis.Redis(host=host,port=port,password=PASSWORD)
        else:
            self._db = redis.Redis(host=host,port=port)


    def get(self,count=1):
        """get proxies from redis"""
        # 从左侧提取ip
        proxies = self._db.lrange('proxies',0,count-1)

        #筛选完后放在右侧
        self._db.ltrim('proxies',count,-1)

        return proxies

    def put(self,proxy):

        """add proxy to right top"""
        self._db.lpush('proxies',proxy)

    def pop(self):

        """get one proxy from right"""
        try:
            self._db.lpop('proxies').decode('utf-8')
        except:
            raise PoolEmptyError
            # 讲一个方法变成属性调用

    @property
    def queue_len(self):
        """get queue's len"""
        return self._db.llen('proxies')

    def flush(self):
        """flush db"""
        self._db.flushall()



