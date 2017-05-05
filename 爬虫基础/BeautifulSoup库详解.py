
"""
作者：文文
内容：BeautifulSoup库
来源:崔庆才老师爬虫实战课程
版本: Python3.5
"""

"""
BeautifulSoup
灵活又方便的网页解析库
安装 pip3 install beautifulsoup4

"""
"""
提供的解析库
1、python标准库 BeautifulSoup(markup,'html.parser') python的内置标准库，执行速度适中，文档容错能力强
2、lxml HTML解析器 BeautifulSoup(markup,'lxml') 速度快，文档容错能力强
3、lxml XML解析器 BeautifulSoup(markup,'xml') 速度快，唯一支持XML的解析器
4、html5lib BeautifulSoup(markup,'html5lib') 最好的容错性、以浏览器的方式解析文档，生成HTML5格式的文档
"""
"""基本用法"""


html="""
    <html><head><title>The Document's story</title></head>
    <body>
    <p class="title" name="dromouse"><b>The Dormouse's story</b></p>
    <p class="story"> Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1"><!--Elsle--></a>,
    <a href="http://example.com/lacle" class="sister" id="link2">Lacle</a>
    <a href="http://example.com/tillle" class="sister" id="link3">Tillle</a>;
    and they lived at hte bottom of a well.</p>
    <p class="story">...</p>
"""

from bs4 import BeautifulSoup
soup = BeautifulSoup(html,'lxml')
print (soup.prettify()) #格式化
print (soup.title.string)


"""标签选择器"""

#选择元素：只返回第一个匹配的标签
soup = BeautifulSoup(html,'lxml')
print (soup.title) #输出title标签
print (type(soup.title)) #<class 'bs4.element.Tag'>
print (soup.head) #<head><title>The Document's story</title></head>
#<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
#只输出第一个p标签
print (soup.p)

#获取标签名称
print (soup.title.name)

#获取属性
#output : dromouse
print(soup.p.attrs['name'])
print (soup.p['name'])

#获取内容
#output : The Dormouse's story
print (soup.p.string)

#嵌套选择
# output : The Document's story
print (soup.head.title.string)

#子节点和子孙节点
html="""
    <html><head><title>The Document's story</title></head>
    <body>

    <p class="story"> Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1"><!--Elsle--></a>,
    <a href="http://example.com/lacle" class="sister" id="link2">Lacle</a>
    <a href="http://example.com/tillle" class="sister" id="link3">Tillle</a>;
    and they lived at hte bottom of a well.</p>
    <p class="story">...</p>
"""
soup = BeautifulSoup(html,'lxml')
#输出p中所有的子节点，输出是一个列表
print(soup.p.contents)

# children 返回迭代器，而不是一个列表
print (soup.p.children)
for i,child in enumerate(soup.p.children):
    print (i,child)

#获取子孙节点，返回一个迭代器
print (soup.p.descendants)
for i,child in enumerate(soup.p.descendants):
    print (i,child)

#获取父节点
print (soup.a.parent)

#获取祖先节点
print (list(enumerate(soup.a.parents)))

#获取兄弟节点
print(list(enumerate(soup.a.next_siblings)))
print (list(enumerate(soup.a.previous_siblings)))


"""标准选择器
find_all(name,attrs,recursive,text,**kwargs)
可根据标签名，属性，内容查找文档
find(name,attrs,recursive,text,**kwargs) 返回单个元素
"""

html ="""
    <div class="panel">
        <div class="panel-heading">
            <h4>Hello</h4>
        </div>
        <div class="panel-body">
            <ul class="list" id="list-1" name="elements">
               <li class="element">Foo</li>
               <li class="element">Bar</li>
               <li class="element">Jay</li>
            </ul>
            <ul class="list list-small" id="list=2">
                <li class="element">Foo</li>
               <li class="element">Bar</li>
            </ul>
        </div>
    </div>
"""

soup = BeautifulSoup(html,'lxml')
#返回ul的列表，包括其里面的内容
print (soup.find_all('ul'))
#<class 'bs4.element.Tag'>
print (type(soup.find_all('ul')[0]))

#迭代提取
for ul in soup.find_all('ul'):
    print (ul.find_all('li'))

#根据属性进行获取
print (soup.find_all(attrs={'id':'list-1'}))
print (soup.find_all(attrs={'name':'elements'}))


#特殊属性如id和class
print (soup.find_all(id="list-1"))
print (soup.find_all(class_='element')) #class需要加一个下划线，因为class是python中的关键字

#根据内容进行选择
#output :['Foo', 'Foo']
print (soup.find_all(text="Foo"))

print (soup.find('ul'))
print (soup.find('page'))

"""其他方法
find_parents()
find_parent()
find_next_siblings()
find_next_sibling()
find_previous_siblings()
find_previous_sibling()
find_all_next()
find_next()
find_all_previous()
find_previous()
"""


"""CSS选择器
通过select()直接传入CSS选择器即可完成选择
"""

html ="""
    <div class="panel">
        <div class="panel-heading">
            <h4>Hello</h4>
        </div>
        <div class="panel-body">
            <ul class="list" id="list-1" name="elements">
               <li class="element">Foo</li>
               <li class="element">Bar</li>
               <li class="element">Jay</li>
            </ul>
            <ul class="list list-small" id="list=2">
                <li class="element">Foo</li>
               <li class="element">Bar</li>
            </ul>
        </div>
    </div>
"""
soup = BeautifulSoup(html,'lxml')
#使用class进行选择加.
print (soup.select('.panel .panel-heading'))
#使用标签进行选择
print (soup.select('ul li'))
#使用id进行选择时，加一个#
print (soup.select('#list-2 .element'))
#output : <class 'bs4.element.Tag'>
print(type(soup.select('ul')[0]))

#迭代选择
for ul in soup.select('ul'):
    print (ul.select('li'))

#获取属性
for ul in soup.select('ul'):
    print(ul['id'])
    print (ul.attrs['id'])

#获取内容
for li in soup.select('li'):
    print(li.get_text())

