# import orjson
# from yfinance import Ticker
#
# from mixin import Mixin
# from protocols.finance_protocol import FinanceProtocol
# from schemas import TickerSchema
#
#
# class FinanceService(Mixin, FinanceProtocol):
#     async def retrieve_ticker_data(self, ticker: str) -> dict | None:
#         result: Ticker = self.get_ticker_data(ticker=ticker)
#         return TickerSchema(ticker=ticker, **orjson.loads(result.fast_info.toJSON())).dict(by_alias=True) \
#             if await self.if_ticker_exist(ticker=ticker) \
#             else None
#
#     @staticmethod
#     async def return_ticker_data(name: str, data) -> dict | None:
#         try:
#             return TickerSchema(ticker=name, **orjson.loads(data.fast_info.toJSON())).dict(by_alias=True)
#         except Exception as e:
#             print(e)
#             return None
#
#     async def retrieve_tickers_data(self, tickers: list[str]) -> list[dict]:
#         tickers_data: dict = self.get_tickers_data(tickers=tickers)
#         return [
#             obj for obj in [
#                 await self.return_ticker_data(name=ticker_name, data=ticker_data)
#                 for ticker_name, ticker_data in tickers_data.items() if await self.if_ticker_exist(ticker_name)
#             ] if obj is not None
#         ]
