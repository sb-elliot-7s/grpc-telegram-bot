import datetime

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    user_id: int = Field(alias='id')
    username: str | None
    first_name: str | None
    last_name: str | None
    date_created: datetime.datetime

    @property
    def to_dict(self): return self.dict()


class FinancialStatementRequestSchema(BaseModel):
    symbol: str
    email: str | None = None


class FinancialStatementResponseSchema(BaseModel):
    symbol: str
    pdf: bytes
    year: str
