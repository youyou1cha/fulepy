#!/usr/bin/env python
# -*- coding: utf-8 -*-

def simple_coroutine():
    print('-> croutine started')
    x = yield
    print('-> croutine received:', x)
    yield


if __name__ == '__main__':
    my_coro = simple_coroutine()
    next(my_coro)
    my_coro.send(42)