"""
作者：文文
内容：python generator
版本: Python3.5
"""

"""
生成器是一个函数，它并不执行并返回一个单一值，而是按照顺序返回一个或多个值
生成器函数执行直到被通知输出一个值，然后会继续执行直到再次被通知输出值
这样持续执行到函数完成或者生成器之上的迭代器终止
"""

"""生成器函数的特征就是在函数内部有一个或多个yield语句，恶如不是return语句
python2中yield和return语句不能共存，但在python3中可以
"""

"""yield语句命令函数返回一个值给调用者，但yield语句不终止函数的执行，执行会暂停直到调用代码重新恢复生成器，在停止的地方再次开始执行"""

"""一个生成器的例子:生成斐波那契数列"""

def fibonacci():
    numbers = []
    while True:
        if len(numbers) < 2:
            numbers.append(1)
        else:
            numbers.append(sum(numbers))
            numbers.pop(0)
        yield numbers[-1]

"""next函数"""
"""
有时候我们想通过生成器得到一个单一的值或者固定数量的值，python提供了内置的next函数，能够让生成器请求他的下一个值
"""
#返回斐波那契数列的前五个值
gen = fibonacci()
for i in range(10):
    print (next(gen))

"""上面的函数是这样执行的，进入for循环，此时i=1，第一次调用next启动我们的生成器，
生成器执行到yield，并返回一个1，此时打印输出，此时for 循环继续，i=2，再次调用next
会继续执行fibonacci()生成器，从yield地方继续执行，下一步是判断while的条件，继续执行到
yield，再次返回一个1，依次类推
"""

"""StopIteration异常"""
"""当使用带有生成器的其他函数时，可以有多条潜在的退出路径，
python2中，return和yield不能共存，此时，python提供了一个内置的异常StopIteration,迭代生成器并且抛出StopIteration异常时，标志着生成器迭代完成
并且自己退出，在这种情况下捕获异常，并且没有回溯。
"""
def my_generator():
    yield 1
    yield 2
    raise StopIteration
    yield 3

#仅返回[1, 2]
print([i for i in my_generator()])

"""然而在python3中，return已经可以与yield共存，有效的使用return实际上等同于raise StopIteration的功能
值得注意的是，如果在return语句中返回一个值，它也不会成为最终输出的值，相反，这个值回会被作为异常信息发送
"""

#下面两个语句等同
# return 42
# raise StopIteration(42)

#但与下面的语法不同
# yield 42
# return


"""生成器之间的交互，send方法"""
"""生成器的协议提供了一个额外的send方法，该方法允许生成器的反向沟通，如果使用send方法而不是使用next方法重启生成器，那么提供给send方法的值实际上能被赋值
给yield表达式的结果"""

def squares(cursor=1):
    while True:
        response = yield cursor ** 2
        if response:
            cursor = int(response)
        else:
            cursor += 1
"""这里，next(gen)，相当于gen.send(None)"""
gen = squares()
#1
print (next(gen))
#4
print (next(gen))
#49
print (gen.send(7))
#64
print (next(gen))









