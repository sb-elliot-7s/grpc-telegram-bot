from abc import ABC, abstractmethod
from dataclasses import dataclass


class FinanceProtocol(ABC):
    @abstractmethod
    async def retrieve_ticker_data(self, ticker: str) -> dict: pass

    @abstractmethod
    async def retrieve_tickers_data(self, tickers: list[str]) -> list[dict]: pass


class NewsTickerProtocol(ABC):
    @abstractmethod
    async def retrieve_news(self, ticker: str) -> list[dict] | None: pass


@dataclass
class IFinanceServiceDecorator(FinanceProtocol):
    service: FinanceProtocol

    async def retrieve_ticker_data(self, ticker: str) -> dict:
        return await self.service.retrieve_ticker_data(ticker=ticker)

    async def retrieve_tickers_data(self, tickers: list[str]) -> list[dict]:
        return await self.service.retrieve_tickers_data(tickers=tickers)
