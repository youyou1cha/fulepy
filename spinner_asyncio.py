#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import itertools
import time
import sys

# 调试 说明是异步函数

async def spin(msg):
    write, flush = sys.stdout.write,sys.stdout.flush
    # 重复迭代元素迭代器
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            # time sleep不能用 要用yield from 交出控制权暂停
            yield from asyncio.sleep(0.1)
        # 捕捉异常退出 cancel
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))


async def slow_function():
    # 一样
    yield  from asyncio.sleep(3)
    return 42


async def supervisor():
    # 异步任务
    spinner = asyncio.create_task(spinner('thinking'))
    print('spinner object:',spinner)
    # 异步启动
    result = yield  from slow_function()
    spinner.cancel()
    return result

def main():
    # 获取事件循环引用
    loop = asyncio.get_event_loop()
    # 获取结果
    result = loop.run_until_complete(supervisor())
    loop.close()
    print('Answer:', result)

if __name__ == '__main__':
    main()
