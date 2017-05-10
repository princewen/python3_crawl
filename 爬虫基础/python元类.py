"""
作者：文文
内容：python元类
来源:崔庆才老师爬虫实战课程
版本: Python3.5
"""

"""！！！类也是对象！！！"""
"""
在理解元类之前，你需要先掌握Python中的类。Python中类的概念借鉴于Smalltalk，这显得有些奇特。在大多数编程语言中，类就是一组用来描述如何生成一个对象的代码段。在Python中这一点仍然成立：
"""

class ObjectCreator(object):
    pass

my_object = ObjectCreator()
#<__main__.ObjectCreator object at 0x100645a58>
print (my_object)

"""
但是，Python中的类还远不止如此。类同样也是一种对象。是的，没错，就是对象。只要你使用关键字class，Python解释器在执行的时候就会创建一个对象。下面的代码段：
class ObjectCreator(object):
    pass

将在内存中创建一个对象，名字就是ObjectCreator。这个对象（类）自身拥有创建对象（类实例）的能力，而这就是为什么它是一个类的原因。但是，它的本质仍然是一个对象，于是乎你可以对它做如下的操作：
1)   你可以将它赋值给一个变量
2)   你可以拷贝它
3)   你可以为它增加属性
4)   你可以将它作为函数参数进行传递
"""
#<class '__main__.ObjectCreator'>
#你可以打印一个类，因为它其实也是一个对象
print (ObjectCreator)

## 你可以将类做为参数传给函数
def echo(o):
    print (o)
# <class '__main__.ObjectCreator'>
echo(ObjectCreator)

#可以为它增加属性
print (hasattr(ObjectCreator,'new_attribute'))
ObjectCreator.new_attribute='foo'
print (hasattr(ObjectCreator,'new_attribute'))
print (ObjectCreator.new_attribute)

#可以将类赋值给一个变量
ObjectCreatorMirror = ObjectCreator
#<__main__.ObjectCreator object at 0x1025384e0>
print (ObjectCreatorMirror())


"""!!!动态地创建类！！！"""
"""因为类也是对象，你可以在运行时动态的创建它们，就像其他任何对象一样。首先，你可以在函数中创建类，使用class关键字即可。"""

def choose_class(name):
    if name=="foo":
        class Foo(object):
            pass
        return Foo
    else:
        class Bar(object):
            pass
        return Bar

MyClass = choose_class('foo')
#<class '__main__.choose_class.<locals>.Foo'>
#打印的是类，而不是类的实例
print (MyClass)

"""但这还不够动态，因为你仍然需要自己编写整个类的代码。
由于类也是对象，所以它们必须是通过什么东西来生成的才对。
当你使用class关键字时，Python解释器自动创建这个对象。
但就和Python中的大多数事情一样，Python仍然提供给你手动处理的方法。
还记得内建函数type吗？这个古老但强大的函数能够让你知道一个对象的类型是什么，
就像这样："""

print (type(1))
print (type('1'))
print (type(ObjectCreator))
print (type(ObjectCreator()))

"""
这里，type有一种完全不同的能力，它也能动态的创建类。type可以接受一个类的描述作为参数，然后返回一个类。
（我知道，根据传入参数的不同，同一个函数拥有两种完全不同的用法是一件很傻的事情，但这在Python中是为了保持向后兼容性）

type可以像这样工作：
type(类名, 父类的元组（针对继承的情况，可以为空），包含属性的字典（名称和值）

"""

MyShinyClass = type('MyShinyClass',(),{})
# <class '__main__.MyShinyClass'>
print (MyShinyClass)
# <__main__.MyShinyClass object at 0x1019b47f0>
print (MyShinyClass())

"""
type 接受一个字典来为类定义属性，因此
class Foo(object):
      bar = True
可以翻译为：
"""
Foo = type('Foo',(),{'bar':True})
#可以把foo当作一个普通的类一样使用
print (Foo)
print (Foo.bar)

f= Foo()
print (f)
print (f.bar)

#当然也可以向这个类继承：
# class Foochild(Foo):
#     pass
Foochild = type('Foochild',(Foo,),{})
print (Foochild.bar)

"""你可以看到，在Python中，类也是对象，你可以动态的创建类。这就是当你使用关键字class时Python在幕后做的事情，而这就是通过元类来实现的。"""


"""！！！元类！！！"""


"""元类就是用来创建类的“东西”。你创建类就是为了创建类的实例对象，不是吗？
但是我们已经学习到了Python中的类也是对象。好吧，元类就是用来创建这些类（对象）的，
元类就是类的类。
函数type实际上是一个元类。type就是Python在背后用来创建所有类的元类。
现在你想知道那为什么type会全部采用小写形式而不是Type呢？好吧，我猜这是为了和str保持一致性，
str是用来创建字符串对象的类，而int是用来创建整数对象的类。type就是创建类对象的类。
你可以通过检查__class__属性来看到这一点。Python中所有的东西，注意，我是指所有的东西——都是对象。
这包括整数、字符串、函数以及类。它们全部都是对象，而且它们都是从一个类创建而来。
"""
age = 35
#<class 'int'>
print (age.__class__)
#<class 'type'>
print (age.__class__.__class__)

"""!!!__metaclass__属性！！！"""

"""你可以在写一个类的时候为其添加__metaclass__属性。
如果你这么做了，Python就会用元类来创建类Foo。小心点，这里面有些技巧。
你首先写下class Foo(object)，但是类对象Foo还没有在内存中创建。
Python会在类的定义中寻找__metaclass__属性，如果找到了，Python就会用它来创建类Foo，
如果没有找到，就会用内建的type来创建这个类。把下面这段话反复读几次。当你写如下代码时 :
class Foo(Bar):
    pass
Python做了如下的操作：
Foo中有__metaclass__这个属性吗？如果是，Python会在内存中通过__metaclass__创建一个名字为Foo的类对象（我说的是类对象，请紧跟我的思路）。
如果Python没有找到__metaclass__，它会继续在Bar（父类）中寻找__metaclass__属性，并尝试做和前面同样的操作。
如果Python在任何父类中都找不到__metaclass__，它就会在模块层次中去寻找__metaclass__，并尝试做同样的操作。
如果还是找不到__metaclass__,Python就会用内置的type来创建这个类对象。
现在的问题就是，你可以在__metaclass__中放置些什么代码呢？答案就是：可以创建一个类的东西。那么什么可以用来创建一个类呢？
type，或者任何使用到type或者子类化type的东东都可以。

"""


"""!!!自定义元类!!!"""

"""
元类的主要目的就是为了当创建类时能够自动地改变类。通常，你会为API做这样的事情，你希望可以创建符合当前上下文的类。假想一个很傻的例子，你决定在你的模块里所有的类的属性都应该是大写形式。有好几种方法可以办到，但其中一种就是通过在模块级别设定__metaclass__。采用这种方法，这个模块中的所有类都会通过这个元类来创建，我们只需要告诉元类把所有的属性都改成大写形式就万事大吉了。
幸运的是，__metaclass__实际上可以被任意调用，它并不需要是一个正式的类（我知道，某些名字里带有‘class’的东西并不需要是一个class，画画图理解下，这很有帮助）。所以，我们这里就先以一个简单的函数作为例子开始。
"""


def upper_attr(future_class_name,future_class_parent,future_class_attr):
    attrs = ((name,value) for name,value in future_class_attr.items if not name.startwith('__'))
    uppercase_attr = dict((name.upper(),value) for name,value in attrs)
    print (uppercase_attr)
    return type(future_class_name,future_class_parent,uppercase_attr)


class Foo(object):
    __metaclass__ = upper_attr
    bar = 'bip'

print (hasattr(Foo,'bar'))

print (hasattr(Foo,'BAR'))

f = Foo()
#print (f.BAR)


# 请记住，'type'实际上是一个类，就像'str'和'int'一样
# 所以，你可以从type继承
class UpperAttrMetaClass(type):
    # __new__ 是在__init__之前被调用的特殊方法

    # __new__是用来创建对象并返回之的方法

    # 而__init__只是用来将传入的参数初始化给对象

    # 你很少用到__new__，除非你希望能够控制对象的创建

    # 这里，创建的对象是类，我们希望能够自定义它，所以我们这里改写__new__

    # 如果你希望的话，你也可以在__init__中做些事情

    # 还有一些高级的用法会涉及到改写__call__特殊方法，但是我们这里不用
    def __new__(upperattr_metaclass, future_class_name, future_class_parents, future_class_attr):
        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
        return type(future_class_name, future_class_parents, uppercase_attr)


# 但是，这种方式其实不是OOP。我们直接调用了type，而且我们没有改写父类的__new__方法。现在让我们这样去处理:
class UpperAttrMetaclass(type):
    def __new__(upperattr_metaclass, future_class_name, future_class_parents, future_class_attr):
        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)

        # 复用type.__new__方法

        # 这就是基本的OOP编程，没什么魔法
        return type.__new__(upperattr_metaclass, future_class_name, future_class_parents, uppercase_attr)

"""
你可能已经注意到了有个额外的参数upperattr_metaclass，这并没有什么特别的。
类方法的第一个参数总是表示当前的实例，就像在普通的类方法中的self参数一样。
当然了，为了清晰起见，这里的名字我起的比较长。但是就像self一样，所有的参数都有它们的传统名称。
因此，在真实的产品代码中一个元类应该是像这样的：
"""
class UpperAttrMetaclass(type):
    def __new__(cls, name, bases, dct):
        attrs = ((name, value) for name, value in dct.items() if not name.startswith('__'))
        uppercase_attr  = dict((name.upper(), value) for name, value in attrs)
        return type.__new__(cls, name, bases, uppercase_attr)
#如果使用super方法的话，我们还可以使它变得更清晰一些，这会缓解继承（是的，你可以拥有元类，从元类继承，从type继承）
class UpperAttrMetaclass(type):
    def __new__(cls, name, bases, dct):
        attrs = ((name, value) for name, value in dct.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
        return super(UpperAttrMetaclass, cls).__new__(cls, name, bases, uppercase_attr)




