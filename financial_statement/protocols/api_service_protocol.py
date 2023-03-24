from abc import ABC, abstractmethod

import grpc


class FinancialStatementServiceProtocol(ABC):
    @abstractmethod
    async def get_financial_statement_data(self, ticker: str):
        pass

    @abstractmethod
    async def get_report(self, symbol: str, context: grpc.aio.ServicerContext) -> dict: pass
