from dataclasses import dataclass, field

import aioredis
import orjson
from aioredis import Redis


@dataclass
class RedisDecorator:
    host: str
    port: int
    redis: Redis = field(init=False)

    def __post_init__(self):
        self.redis = aioredis.from_url(f'redis://{self.host}:{self.port}')

    def cache(self, ex: int = 60):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                key = kwargs.get('ticker')
                result = await self.redis.get(key)
                if not result:
                    data = await func(*args, **kwargs)
                    await self.redis.set(name=key, value=orjson.dumps(data), ex=ex)
                    return data
                return orjson.loads(result)

            return wrapper

        return decorator

    async def _save_tickers_to_cache(self, data: list, ex: int, from_api: bool = False):
        for value in data:
            await self.redis.set(
                name=value.get('symbol' if from_api else 'ticker').lower(),
                value=orjson.dumps(value),
                ex=ex
            )

    def cache_many_tickers(self, ex: int = 60, from_api: bool = False):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                keys: list[str] = kwargs.get('tickers')
                count_of_tickers: int = len(keys)
                cache: list[str | None] = [await self.redis.get(name=key) for key in keys]
                result = [x for x in cache if x is not None]
                if not len(result):
                    data = await func(*args, **kwargs)
                    await self._save_tickers_to_cache(data=data, ex=ex, from_api=from_api)
                    return data
                cached_tickers: list[dict] = [orjson.loads(ticker) for ticker in result]
                ticker_symbols_in_cache: list[str] = [
                    t.get('symbol' if from_api else 'ticker').lower() for t in cached_tickers
                ]
                if len(cached_tickers) != count_of_tickers:
                    not_in_cache_ticker: list[str] = list(set(keys) - set(ticker_symbols_in_cache))
                    data = await func(*args, tickers=not_in_cache_ticker)
                    await self._save_tickers_to_cache(data=data, ex=ex, from_api=from_api)
                    return cached_tickers + data
                return cached_tickers

            return wrapper

        return decorator
