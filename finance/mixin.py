import aiohttp
import yfinance as yf


class Mixin:
    @staticmethod
    def get_ticker_data(ticker: str):
        return yf.Ticker(ticker=ticker)

    @staticmethod
    def get_tickers_data(tickers: list[str]) -> dict:
        return yf.Tickers(tickers=tickers).tickers

    @staticmethod
    async def if_ticker_exist(ticker: str) -> bool:
        url = f'https://finance.yahoo.com/quote/{ticker.upper()}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, allow_redirects=False) as response:
                return True if response.status == 200 else False
