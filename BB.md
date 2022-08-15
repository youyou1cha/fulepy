# asyncio

> 并发是指一次处理多件事
> 并行是指一次做很多事情
>
> 使用不同的词表示相同的事物，使用同一个词表示不同的事物

## 协程

协程是微线程，利用了硬件的中断的概念。

协程利用用户态的上下文切换，就是利用进程中的自带运行上下文配合中断来回切换函数方法；

await 会创建一个协程，然后等待结果返回；

await是个流程控制关键字；

* 事件循环

* 协程
  * asyncio
  * async & await

* Task对象

* Fututer对象

* 异步迭代器
  * __anext__ __aiter__

* 异步上下文管理器
  * __aenter__  __aexit__

```python
# 常用方法和流程
# async & await 个人认为就是一种流程控制；把同步的方法编程协程对象；然后放到事件循环里面。来通过进程中断来提高IO或者网络效率
# 写的方法就是先写一下同步流程。然后再同步需要等待的方法改成async方法；
# 流程上需要等待的方法，加上await
# 最后方法加入task里面然后通过run或者create_task或者loop.as_unit_commpet等方法执行完成；
import asyncio
import aioredis

async def main():
    redis = await aioredis.create_redis_pool('redis://localhost')
    await redis.hmset_dict('hash',key='value',key='vaule',key3=1234)
    result = awat redis.hgetall('hash',encoding='utf-8')
    assert result = {
        'key1':'value1',
        'key2':'value2',
        'key3':1234
    }
    redis.close()
    await redis.wait_closed()

asyncio.run(main())

```





