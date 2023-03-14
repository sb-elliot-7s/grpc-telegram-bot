from pydantic import BaseModel

from configs import get_configs


class FinancialStatementSchema(BaseModel):
    symbol: str
    email: str


class FinancialStatementResponseSchema(BaseModel):
    symbol: str
    pdf: bytes
    year: str


class EmailDataSchema(BaseModel):
    pdf: bytes
    text: str
    to_user: str
    year: str
    from_user: str = get_configs().from_user
    email_host: str = get_configs().email_host
    email_port: int = get_configs().email_port
    email_password: str = get_configs().email_password
