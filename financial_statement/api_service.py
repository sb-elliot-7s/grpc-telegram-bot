from dataclasses import dataclass

import aiohttp
import grpc

from configs import get_configs
from decorators import CacheRedis
from protocols.api_service_protocol import FinancialStatementServiceProtocol


@dataclass
class APIFinancialStatementService(FinancialStatementServiceProtocol):
    base_url: str = get_configs().base_url

    app_redis = CacheRedis(host=get_configs().redis_host, port=get_configs().redis_port)
    ONE_DAY = 86400

    @app_redis.cache(exp_time=ONE_DAY)
    async def get_financial_statement_data(self, ticker: str) -> list[dict] | None:
        api_token = get_configs().api_token
        path = f'/api/v3/sec_filings/{ticker.upper()}?type=10-K&page=0&apikey={api_token}'
        async with aiohttp.ClientSession(base_url=self.base_url) as session:
            async with session.get(url=path) as response:
                if response.status != 200:
                    return None
                return await response.json()

    async def get_report(self, symbol: str, context: grpc.aio.ServicerContext) -> dict:
        last_report = 0
        reports: list[dict] | None = await self.get_financial_statement_data(ticker=symbol)
        if reports is None:
            await context.abort(code=grpc.StatusCode.INVALID_ARGUMENT, details='You must pass valid symbol')
        return reports[last_report]
