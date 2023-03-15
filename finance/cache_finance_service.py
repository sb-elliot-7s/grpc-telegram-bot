from configs import get_configs
from decorators import RedisDecorator
from protocols.finance_protocol import IFinanceServiceDecorator


class CacheFinanceService(IFinanceServiceDecorator):
    redis_decorator = RedisDecorator(host=get_configs().redis_host, port=get_configs().redis_port)

    @redis_decorator.cache(ex=get_configs().ticker_exp_minute * 10)
    async def retrieve_ticker_data(self, ticker: str) -> dict:
        return await super().retrieve_ticker_data(ticker=ticker)

    @redis_decorator.cache_many_tickers(ex=get_configs().ticker_exp_minute * 10, from_api=True)
    async def retrieve_tickers_data(self, tickers: list[str]) -> list[dict]:
        return await super().retrieve_tickers_data(tickers=tickers)
