import yfinance as yf
from yfinance import Ticker

from decorators import cache
from protocols.finance_protocol import FinanceProtocol, NewsTickerProtocol, IFinanceServiceDecorator
from schemas import NewsSchema, TickerSchema


class Mixin:
    @staticmethod
    def get_ticker(ticker: str):
        return yf.Ticker(ticker=ticker)


class CacheFinanceService(IFinanceServiceDecorator):

    @cache(ex=10)
    async def retrieve_ticker_data(self, ticker: str) -> dict:
        return await super().retrieve_ticker_data(ticker)


class FinanceService(Mixin, FinanceProtocol):
    async def retrieve_ticker_data(self, ticker: str) -> dict:
        result: Ticker = self.get_ticker(ticker=ticker)
        return TickerSchema.parse_raw(result.fast_info.toJSON()).dict(by_alias=True)


class NewsService(Mixin, NewsTickerProtocol):
    async def retrieve_news(self, ticker: str) -> list[dict] | None:
        result: Ticker = self.get_ticker(ticker=ticker)
        news: list[dict] = result.news
        if not len(news):
            return None
        return [NewsSchema(**n).dict(by_alias=True) for n in news]
