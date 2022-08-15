#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 异步
import asyncio
import  time

# 分两步，添加和执行；下一个执行不能等上一个添加结束

async  def add_clothes():
    print('往洗衣机里面添加衣服')
    await asyncio.sleep(3)
# 洗衣服
async def washing1():
    print('洗衣服工作之前，需加衣服进去')
    # 等待这个完成
    await add_clothes()
    print('衣服加进去了，可以工作了。。。')
    # 等待这个完成
    await asyncio.sleep(3)
    print('washer1 finished')
# 异步是利用协程对象，不能直接运行。需要放到事件循环里面

print('start washing')
start_time = time.time()
task = washing1()
loop = asyncio.get_event_loop()
result = loop.run_until_complete(task)
end_time = time.time()
print('-------------end washing---------')
print('time {}'.format(end_time - start_time))

# 该着程序流程。利用await。让他等待结果去执行其他协程。等有结果了再过来执行；
# 就是事件循环执行的方法
