#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import  namedtuple
from typing import Mapping as map

Result = namedtuple('Result','count average')

# 子生成器
def averager():
    total = 0.0
    count = 0
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total / count
        # print(average)
    return Result(count, average)

# 委托生成器
# 这个就是.NET的委托啊
def grouper(results,key):
    while True:
        results[key] = yield from averager()

# 客户端代码 调用方
def main(data:map[str,any]):
    results = {}
    for key ,values in data.items():
        group = grouper(results,key)
        next(group)
        for value in values:
            group.send(value)
        group.send(None) # 停止
    print(results)
    # report(results)
# 如果不用yield from
def main1(data):

    # _i = iter(averager())
    # try:
    #     _y = next(_i)
    # except StopIteration as _e:
    #     _r = _e.value
    # else:
    #     while 1:
    #         _s = yield  _y
    #         try:
    #             _y = _i.send(_s)
    #         except StopIteration as _e:
    #             _r = _e.value
    #             break
    # res = _r
    # print(res)
    result = {}
    for key ,values in data.items():
        res = averager()
        next(res)
        try:
            for value in values:
                    res.send(value)
            res.send(None)
        except StopIteration as _e:
            result[key] = _e.value
    print(result)
def report(results):
    for key,result in sorted(results.items()):
        group , unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(result.count,group,result.average,unit))


data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}
if __name__ == '__main__':
    main1(data)
    main(data)

# 对人类来说，几乎所有最重要的信息都在靠近顶部的某个段落里。
# 把迭代器当成生成器使用，相当于把子生成器的定义体内联在yield from表达式中，此外，子生成器可以执行return语句。返回一个值。而返回的值成为yield from 表达式的值