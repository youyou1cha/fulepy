#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 异步

# redis

import asyncio
import aiomysql
import aioredis

async  def main1():
    redis = await  aioredis.create_redis_pool('redis://localhos')
    await redis.get('my-key','value')
    value = await redis.get('my-key',encodings='utf-8')
    print(value)

    redis.close()
    await redis.wait_closed()
asyncio.run(main1())

loop = asyncio.get_event_loop()

async def text_example():
    conn = await aiomysql.connect(host='127.0.0.1',port=3306 **)
    cur = await conn.cursor()
    await cur.execute('select * from user')
    print(cur.description)
    r = await cur.fetchall()
    print(r)
    await cur.close()
    conn.close()
loop.run_until_complete(text_example())