
"""
作者：文文
内容：正则表达式
来源:崔庆才老师爬虫实战课程
版本: Python3.5
"""

"""

正则表达式是对字符串操作的一种逻辑公式，就是用事先定义
好的一些特定字符，及这些特定字符的组合，组成一个"规则
字符串"，这个"规则字符串"用来表达对字符串的一种过滤逻辑

"""

import re

"""
match函数,检验正则表达式与字符串是否匹配
它会从第一个字符开始匹配，这是不方便的地方
"""

content = "Hello 123 4567 World_This is a Regex Demo"
#最常规的匹配
result = re.match('^Hello\s\d\d\d\s\d{4}\s\w{10}.*$',content)
# output : <_sre.SRE_Match object; span=(0, 41), match='Hello 123 4567 World_This is a Regex Demo'>
print (result)
#输出匹配结果
print (result.group())
#输出匹配位置
print (result.span())


#泛匹配
result= re.match('^Hello.*Demo$',content)
print (result)

#匹配目标
result = re.match(r'^Hello\s(\d+\s\d+)\sWorld.*Demo$',content)
print (result.group(1))

#非贪婪匹配
content = "Hello 1234567 World_This is a Regex Demo"
result = re.match(r'^Hello.*(\d+)\sWorld.*Demo$',content)
#输出7，.*尽可能多的匹配
print (result.group(1))
#输出1234567，非贪婪模式
result = re.match(r'^Hello.*?(\d+)\sWorld.*Demo$',content)
#输出7，.*尽可能多的匹配
print (result.group(1))


#匹配模式
content = "Hello 1234567 World_This\n is a Regex Demo"


#转义
content = "price is $5.00"

result = re.match(r'price is $5.00',content)
#Output : None
print (result)
#output : <_sre.SRE_Match object; span=(0, 14), match='price is $5.00'>
result = re.match(r'price is \$5\.00',content)
print (result)


"""
re.search方法
会搜索整个字符串，返回第一个成功的匹配
"""

"""
re.findall方法，搜索字符串，以列表形式返回全部匹配的字串
"""

"""
re.sub方法，三个参数，正则表达式，替换成的字符串，原字符串
"""

"""
re.compile方法，将一个正则表达式串编译成正则对象，以便于复用该匹配模式
"""





