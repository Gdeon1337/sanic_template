from typing import List, Set

import aioredis
from aioredis.errors import ConnectionClosedError
from sanic import Sanic
from tenacity import retry, stop_after_attempt, wait_random


class RedisConn:
    conn = None
    redis_connection = None

    @retry(reraise=True, stop=stop_after_attempt(3), wait=wait_random(min=1, max=3))
    async def connect(self):
        self.conn = await aioredis.create_redis(self.redis_connection)

    async def create_redis_connection(self, app: Sanic, _):
        self.redis_connection = app.config.REDIS_CONNECTION
        await self.connect()

    async def close_redis_connection(self, *args):  # pylint: disable=unused-argument
        if self.conn:
            self.conn.close()
            await self.conn.wait_closed()

    async def zadd(self, *domains, timestamp: int):
        await self.ping()
        pipe = self.conn.pipeline()
        for domain in domains:
            pipe.zadd('ap', timestamp, domain)
        await pipe.execute()

    async def zrange(self, datetime_start: int, datetime_end: int) -> Set:
        await self.ping()
        return await self.conn.zrangebyscore(
            'ap',
            min=datetime_start-1,
            max=datetime_end+1
        )

    async def zrevrange_by_lex(self, datetime_start: int, datetime_end: int) -> Set:
        await self.ping()
        return await self.conn.zrevrangebylex(
            'ap',
            min=f'{datetime_start-1}'.encode('utf-8'),
            max=f'{datetime_end+1}'.encode('utf-8')
        )

    @retry(reraise=True, stop=stop_after_attempt(3))
    async def ping(self):
        if not self.conn:
            await self.connect()
        try:
            await self.conn.ping()
        except BaseException:
            self.conn = None
            raise ConnectionClosedError("Redis conn disconnected")
