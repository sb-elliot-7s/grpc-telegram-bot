from yfinance import Ticker

from mixin import Mixin
from protocols.finance_protocol import NewsTickerProtocol
from schemas import NewsSchema


class NewsService(Mixin, NewsTickerProtocol):
    async def retrieve_news(self, ticker: str) -> list[dict] | None:
        result: Ticker = self.get_ticker_data(ticker=ticker)
        news: list[dict] = result.news
        return None if not len(news) else [NewsSchema(**n).dict(by_alias=True) for n in news]
