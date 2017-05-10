"""
作者：文文
内容：python 协程 Coroutine
版本: Python3.5
"""

"""
子程序，或者称为函数，在所有语言中都是层级调用，比如A调用B，B在执行过程中又调用了C，C执行完毕返回，B执行完毕返回，最后是A执行完毕。

所以子程序调用是通过栈实现的，一个线程就是执行一个子程序。

子程序调用总是一个入口，一次返回，调用顺序是明确的。而协程的调用和子程序不同。

协程看上去也是子程序，但执行过程中，在子程序内部可中断，然后转而执行别的子程序，在适当的时候再返回来接着执行。

注意，在一个子程序中中断，去执行其他子程序，不是函数调用，有点类似CPU的中断。比如子程序A、B：
"""

def A():
    print('1')
    print('2')
    print('3')

def B():
    print('x')
    print('y')
    print('z')

"""假设由协程执行，在执行A的过程中，可以随时中断，去执行B，B也可能在执行过程中中断再去执行A，结果可能是：
1
2
x
y
3
z
"""

"""
但是在A中是没有调用B的，所以协程的调用比函数调用理解起来要难一些。

看起来A、B的执行有点像多线程，但协程的特点在于是一个线程执行，那和多线程比，协程有何优势？

最大的优势就是协程极高的执行效率。因为子程序切换不是线程切换，而是由程序自身控制，因此，没有线程切换的开销，和多线程比，线程数量越多，协程的性能优势就越明显。

第二大优势就是不需要多线程的锁机制，因为只有一个线程，也不存在同时写变量冲突，在协程中控制共享资源不加锁，只需要判断状态就好了，所以执行效率比多线程高很多。

因为协程是一个线程执行，那怎么利用多核CPU呢？最简单的方法是多进程+协程，既充分利用多核，又充分发挥协程的高效率，可获得极高的性能。
"""

"""Python对协程的支持是通过generator实现的。
传统的生产者-消费者模型是一个线程写消息，一个线程取消息，通过锁机制控制队列和等待，但一不小心就可能死锁。

如果改用协程，生产者生产消息后，直接通过yield跳转到消费者开始执行，待消费者执行完毕后，切换回生产者继续生产，效率极高：
"""

def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print ('[CONSUMER] consuming %s...' % n)
        r = '200 OK'

def produce(c):
    # c.send(None) 相当于next(c) ，用于第一次激活生成器
    c.send(None)
    n = 0
    while n<5:
        n = n+1
        print ('[Producer] producing %s...' % n)
        r = c.send(n)
        print ('[Producer] Consumer return : %s' % r)
    c.close()

c=consumer()
produce(c)

"""
返回结果:
[Producer] producing 1...
[CONSUMER] consuming 1...
[Producer] Consumer return : 200 OK
[Producer] producing 2...
[CONSUMER] consuming 2...
[Producer] Consumer return : 200 OK
[Producer] producing 3...
[CONSUMER] consuming 3...
[Producer] Consumer return : 200 OK
[Producer] producing 4...
[CONSUMER] consuming 4...
[Producer] Consumer return : 200 OK
[Producer] producing 5...
[CONSUMER] consuming 5...
[Producer] Consumer return : 200 OK
"""

"""
首先调用c.send(None)启动生成器；

然后，一旦生产了东西，通过c.send(n)切换到consumer执行；

consumer通过yield拿到消息，处理，又通过yield把结果传回；

produce拿到consumer处理的结果，继续生产下一条消息；

produce决定不生产了，通过c.close()关闭consumer，整个过程结束。

整个流程无锁，由一个线程执行，produce和consumer协作完成任务，所以称为“协程”，而非线程的抢占式多任务。


"""

