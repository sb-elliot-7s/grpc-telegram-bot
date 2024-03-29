import datetime
from enum import IntEnum
from typing import Any

import orjson
from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    user_id: int = Field(alias='id')
    username: str | None
    first_name: str | None
    last_name: str | None
    date_created: datetime.datetime

    @property
    def to_dict(self): return self.dict()


class TypePDFResponse(IntEnum):
    PDF_URL = 0
    PDF_BYTES = 1


class FinancialStatementRequestSchema(BaseModel):
    symbol: str
    email: str | None = None
    pdf_response: TypePDFResponse | None = TypePDFResponse.PDF_URL


class FinancialStatementResponseSchema(BaseModel):
    symbol: str
    pdf: bytes | None
    year: str
    pdf_url: str | None


class KafkaSettingsSchema(BaseModel):
    bootstrap_servers: list | str
    value_serializer: Any = lambda x: orjson.dumps(x)
    compression_type: str = 'gzip'
