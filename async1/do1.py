#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 同步

import  time
def wshing1():
    time.sleep(3)
    print('washer1 finished')


def wshing2():
    time.sleep(5)
    print('washer2 finished')


def wshing3():
    time.sleep(8)
    print('washer3 finished')

if __name__ == '__main__':
    stat_time = time.time()
    wshing1()
    wshing2()
    wshing3()
    end_time = time.time()
    print("总共耗时：{}".format(end_time - stat_time))