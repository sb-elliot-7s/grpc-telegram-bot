import aiohttp
import yfinance as yf
from yfinance import Ticker

from decorators import cache
from protocols.finance_protocol import FinanceProtocol, NewsTickerProtocol, IFinanceServiceDecorator
from schemas import NewsSchema, TickerSchema


class Mixin:
    @staticmethod
    def get_ticker(ticker: str):
        return yf.Ticker(ticker=ticker)

    @staticmethod
    async def if_ticker_exist(ticker: str) -> bool:
        url = f'https://finance.yahoo.com/quote/{ticker.upper()}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, allow_redirects=False) as response:
                return True if response.status == 200 else False


class CacheFinanceService(IFinanceServiceDecorator):

    @cache(ex=10)
    async def retrieve_ticker_data(self, ticker: str) -> dict:
        return await super().retrieve_ticker_data(ticker)


class FinanceService(Mixin, FinanceProtocol):
    async def retrieve_ticker_data(self, ticker: str) -> dict | None:
        result: Ticker = self.get_ticker(ticker=ticker)
        return TickerSchema.parse_raw(result.fast_info.toJSON()).dict(by_alias=True) \
            if await self.if_ticker_exist(ticker=ticker) \
            else None


class NewsService(Mixin, NewsTickerProtocol):
    async def retrieve_news(self, ticker: str) -> list[dict] | None:
        result: Ticker = self.get_ticker(ticker=ticker)
        news: list[dict] = result.news
        return None if not len(news) else [NewsSchema(**n).dict(by_alias=True) for n in news]
