#!/usr/bin/env python
# -*- coding: utf-8 -*-

def averager():
    total = 0.0
    count = 0
    averager = None
    while True:
        term = yield averager
        total += term
        count += 1
        averager = total / count
        print(averager)
# 装饰圈
from functools import  wraps
def coroutine(func):

    @wraps(func)
    def primer(*args,**kwargs):
        gen = func(*args,**kwargs)
        next(gen)
        return gen
    return primer
if __name__ == '__main__':
    # coro_avg = averager()
    # # create 协程
    # next(coro_avg)
    # coro_avg.send(10)
    # coro_avg.send(30)
    # coro_avg.send(5)
    coro_avg =