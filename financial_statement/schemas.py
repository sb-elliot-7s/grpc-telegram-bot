from pydantic import BaseModel


class FinancialStatementSchema(BaseModel):
    symbol: str
    email: str


class FinancialStatementResponseSchema(BaseModel):
    symbol: str
    pdf: bytes
    year: str
