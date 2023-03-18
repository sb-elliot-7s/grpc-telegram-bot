from abc import ABC, abstractmethod

from schemas import FinancialStatementRequestSchema


class FinancialStatementServiceProtocol(ABC):
    @abstractmethod
    async def get_financial_statement(self, schema: FinancialStatementRequestSchema):
        pass
