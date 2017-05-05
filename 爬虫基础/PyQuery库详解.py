
"""
作者：文文
内容：PyQuery库
来源:崔庆才老师爬虫实战课程
版本: Python3.5
"""

"""
PyQuery库
强大又灵活的网页解析哭，如果你熟悉jQuery的语法，那么PyQuery非常合适
安装 pip install pyquery
"""

"""初始化"""

html = '''
    <div>
        <ul class='list">
            <li class="item-0">first item</li>
            <li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-0 active"><a href="link3.html">third item</a></li>
            <li class="item-1 active"><a href="link4.html">fourth item</a></li>
        </ul>
    </div>
'''


from pyquery import PyQuery as pq

#字符串初始化
doc = pq(html)
#<li class="item-0">first item</li>
# <li class="item-1"><a href="link2.html">second item</a></li>
# <li class="item-0 active"><a href="link3.html">third item</a></li>
# <li class="item-1 active"><a href="link4.html">fourth item</a></li>
#根据css选择器进行选择
print (doc('li'))


#URL初始化
doc = pq(url="http://www.baidu.com")
print (doc('head'))

#文件初始化
# doc = pq(filename='demo.html')
# print (doc('li'))

"""基本CSS选择器"""

doc = pq(html)
#有层级关系就好
print (doc('#container .list li'))


"""查找元素"""

#查找子元素
doc = pq(html)
items = doc('.list')
print (type(items))
print (items)

lis = items.find('li')
print (type(lis))
print (lis)

lis=items.children()
print (lis)

lis = items.children('.active')
print (lis)

#查找父元素
doc = pq(html)
items = doc('.list')
container = items.parent()
print (container)

#查找祖先元素
parents = items.parents()
print (parents)

parent = items.parents('wrap')
print (parent)

#查找兄弟元素
li = doc('.list .item-0.active')
print (li.siblings())

"""遍历"""

doc = pq(html)
lis = doc('li').items()
for li in lis:
    print (li)


"""获取属性"""

#获取属性
doc = pq(html)
a = doc('.item-0.active a')
print (a.attr('href'))

#获取文本
print (a.text())

#获取HTML
print (a.html())



"""DOM操作"""





