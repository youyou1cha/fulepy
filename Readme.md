# 序列

* 定义__len__ __getitem__方法可以实现序列的鸭子模型
* 动态属性 __setattr__ __getattr__
* python很多属性不和java一样通过继承获得，这个是通过定义__内部函数获得
* zip zip_longest; zip是迭代最短序列；zip_longest是迭代最长序列。通过fillevalue来填充
* dir返回包含方法，变量属性的列表；vars当前环境变量

# 继承

* 多重继承
* 内置类继承 userdict；内置的内置方法，继承类不会变动

# 生成器&迭代器

* 生成器的进化
* 迭代器可以说是生成器的子集
* 归约：合拢 迭代器->单个结果集
  * all
  * any
  * max
  * min
  * reduec
  * sum
* yield from 后面跟着iterable 就可以替代for循环

  主要是__iter__ __getitem__实现以后就可以迭代；通过yield可以写生成器函数；
基础类库里面itertool里面，我用的最多的就是zip enmuerate 其他的用到我再看吧
* 哨符： Iter()方法。当iter到哨符就触发StopIterations

# 上下文管理 with

上下文管理会生成一些临时上下文交给对象控制
__enter__;__exit__;
通过contextlib.contextmanager 配合yield可以实现上下文
# 协程
send方法可以交互
yield from 这行代码会产出一个值，提供给next(...)的调用方；除外做出让步，暂停执行生成器，让调用方继续工作。知道需要使用另外一个值调用next
to yield 给出释义：产出和让步
yield 、 yield with 等都是流程控制语句。和我之前想的for if while感觉不一样

## 还是给协程定义了一个规则，开始 暂停 关闭  GEN_CREATED GEN_RUNNING GEN_SUSPENDED GEN_CLOSED

----

yield from 结构会在内部自动捕获 StopIteration 异常。这种处理方式与
for 循环处理 StopIteration 异常的方式一样：循环机制使用用户易于理解的方式处理异
常。对 yield from 结构来说，解释器不仅会捕获 StopIteration 异常，还会把 value 属性
的值变成 yield from 表达式的值

----
# 闭包和装饰圈
* 闭包必须是嵌套函数
* 嵌套函数必须引用封闭函数定义的值
* 闭包函数必须返回嵌套函数
```python
def a(a):
    def p(p):
        print('----{}'.format(p))
        print('----{}'.format(a))
    return p
ab = a(5)
ab(55)
```





## yield form 

![image-20220813180821391](C:\Users\waw\AppData\Roaming\Typora\typora-user-images\image-20220813180821391.png)

yield from就是一个双向通道。链接调用方caller 和子生成器；通过
