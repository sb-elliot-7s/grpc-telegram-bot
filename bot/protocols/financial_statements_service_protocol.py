from abc import ABC, abstractmethod


class FinancialStatementServiceProtocol(ABC):
    @abstractmethod
    async def get_financial_statement(
            self, symbol: str,
            count_of_years: int = 1,
            email: str | None = None
    ):
        pass
