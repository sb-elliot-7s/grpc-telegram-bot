import json

import aioredis

from configs import get_configs


def cache(ex: int, type_: str | None = 'finance'):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            redis = aioredis.from_url(f'redis://{get_configs().redis_host}:{get_configs().redis_port}')
            key = f"{type_}:{kwargs.get('ticker')}"
            result = await redis.get(key)
            if not result:
                data = await func(*args, **kwargs)
                await redis.set(name=key, value=json.dumps(obj=data, default=str), ex=ex)
                return data
            return json.loads(result)

        return wrapper

    return decorator
