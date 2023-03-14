from abc import ABC, abstractmethod


class FinancialStatementServiceProtocol(ABC):
    @abstractmethod
    async def get_financial_statement_data(self, ticker: str):
        pass
