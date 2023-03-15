from dataclasses import dataclass

from api_service import APIService
from configs import get_configs
from mixin import Mixin
from protocols.finance_protocol import FinanceProtocol
from schemas import TickerSchema


@dataclass
class APIFinanceService(Mixin, FinanceProtocol):
    api_key: str = get_configs().api_token

    async def retrieve_ticker_data(self, ticker: str) -> dict | None:
        result: dict = await APIService(api_key=get_configs().api_token).request(quotes=ticker)
        if not len(result):
            return None
        return TickerSchema(**result[0]).dict(by_alias=True)

    async def retrieve_tickers_data(self, tickers: list[str]) -> list[dict]:
        result: list[dict] = await APIService(api_key=get_configs().api_token).request(quotes=','.join(tickers))
        return [TickerSchema(**t).dict(by_alias=True) for t in result]
