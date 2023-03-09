import json

from yfinance import Ticker

from configs import get_configs
from decorators import RedisDecorator
from mixin import Mixin
from protocols.finance_protocol import FinanceProtocol, IFinanceServiceDecorator
from schemas import TickerSchema


class CacheFinanceService(IFinanceServiceDecorator):
    redis_decorator = RedisDecorator(host=get_configs().redis_host, port=get_configs().redis_port)

    @redis_decorator.cache(ex=60)
    async def retrieve_ticker_data(self, ticker: str) -> dict:
        return await super().retrieve_ticker_data(ticker=ticker)

    @redis_decorator.cache_many_tickers(ex=20)
    async def retrieve_tickers_data(self, tickers: list[str]) -> list[dict]:
        return await super().retrieve_tickers_data(tickers=tickers)


class FinanceService(Mixin, FinanceProtocol):
    async def retrieve_ticker_data(self, ticker: str) -> dict | None:
        result: Ticker = self.get_ticker_data(ticker=ticker)
        return TickerSchema(ticker=ticker, **json.loads(result.fast_info.toJSON())).dict(by_alias=True) \
            if await self.if_ticker_exist(ticker=ticker) \
            else None

    @staticmethod
    async def return_ticker_data(name: str, data) -> dict | None:
        try:
            return TickerSchema(ticker=name, **json.loads(data.fast_info.toJSON())).dict(by_alias=True)
        except Exception as e:
            print(e)
            return None

    async def retrieve_tickers_data(self, tickers: list[str]) -> list[dict]:
        tickers_data: dict = self.get_tickers_data(tickers=tickers)
        return [
            obj for obj in [
                await self.return_ticker_data(name=ticker_name, data=ticker_data)
                for ticker_name, ticker_data in tickers_data.items() if await self.if_ticker_exist(ticker_name)
            ] if obj is not None
        ]
