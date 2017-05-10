"""
作者：文文
内容：asyncio库
版本: Python3.5
"""
"""
asyncio是Python 3.4版本引入的标准库，直接内置了对异步IO的支持。
asyncio的编程模型就是一个消息循环。我们从asyncio模块中直接获取一个EventLoop的引用，然后把需要执行的协程扔到EventLoop中执行，就实现了异步IO。
"""
"""用asyncio实现Hello world代码如下：
"""


import asyncio

@asyncio.coroutine
def hello():
    print ('Hello World')
    r = yield from asyncio.sleep(1)
    print ('Hello again!')


loop = asyncio.get_event_loop()
loop.run_until_complete(hello())
loop.close()

"""
@asyncio.coroutine把一个generator标记为coroutine类型，然后，我们就把这个coroutine扔到EventLoop中执行。

hello()会首先打印出Hello world!，然后，yield from语法可以让我们方便地调用另一个generator。由于asyncio.sleep()也是一个coroutine，所以线程不会等待asyncio.sleep()，而是直接中断并执行下一个消息循环。当asyncio.sleep()返回时，线程就可以从yield from拿到返回值（此处是None），然后接着执行下一行语句。

把asyncio.sleep(1)看成是一个耗时1秒的IO操作，在此期间，主线程并未等待，而是去执行EventLoop中其他可以执行的coroutine了，因此可以实现并发执行。

"""

"""
我们用Task封装两个coroutine试试,执行时需将上面代码注释掉：
"""
import threading
@asyncio.coroutine
def hello():
    print('Hello world! (%s)' % threading.currentThread())
    yield from asyncio.sleep(1)
    print('Hello again! (%s)' % threading.currentThread())

loop = asyncio.get_event_loop()
tasks = [hello(),hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

"""由打印的当前线程名称可以看出，两个coroutine是由同一个线程并发执行的。"""



"""小结：
asyncio提供了完善的异步IO支持；

异步操作需要在coroutine中通过yield from完成；

多个coroutine可以封装成一组Task然后并发执行。
"""
