from dataclasses import dataclass, field

import aioredis
import orjson
from aioredis import Redis


@dataclass
class CacheRedis:
    host: str
    port: int
    redis: Redis = field(init=False)

    def __post_init__(self):
        self.redis = aioredis.from_url(f'redis://{self.host}:{self.port}')

    def cache(self, exp_time: int = 0):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                if (ticker := kwargs.get("ticker")) is None:
                    return None
                key = f'ticker:{ticker}'
                from_cache_data = await self.redis.get(name=key)
                if from_cache_data is None:
                    data = await func(*args, **kwargs)
                    await self.redis.set(ex=exp_time, name=key, value=orjson.dumps(data))
                    return data
                return orjson.loads(from_cache_data)

            return wrapper

        return decorator
