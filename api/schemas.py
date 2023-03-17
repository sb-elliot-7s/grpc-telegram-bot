from typing import Any

from fastapi import Query
from pydantic import BaseModel


class UserSchema(BaseModel):
    user_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    date_created: str
    email: str | None


class QueryParams(BaseModel):
    skip: int | None
    limit: int | None
    date_created: str | None
    operator_date_created: str | None

    @classmethod
    def as_query(
            cls, skip: int | None = Query(None),
            limit: int | None = Query(None),
            date_created: str | None = Query(None),
            operator_date_created: str | None = Query(None)
    ):
        return cls(
            skip=skip,
            limit=limit,
            date_created=date_created,
            operator_date_created=operator_date_created
        )


class RespSchema(BaseModel):
    status_code: int
    response_model: Any
    path: str

    class Config:
        arbitrary_types_allowed = True
