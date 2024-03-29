from datetime import datetime
from typing import Any

import orjson
from fastapi import Query
from pydantic import BaseModel

from constants import GroupID


class UserUpdateSchema(BaseModel):
    user_id: int
    email: str | None


class UserSchema(UserUpdateSchema):
    username: str | None
    first_name: str | None
    last_name: str | None
    date_created: datetime

    class Config:
        json_encoders = {
            datetime: lambda x: x.strftime('%Y:%m:%d %H:%M')
        }

    def to_mongo_obj(self):
        return {'_id': self.user_id, **self.dict(exclude={'user_id'})}

    @classmethod
    def from_mongo_obj(cls, mongo_user: dict):
        return {'user_id': mongo_user.get('_id'), **mongo_user}


class Options(BaseModel):
    skip: int | None
    limit: int | None


class QueryParams(Options):
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


class KafkaSettingsSchema(BaseModel):
    group_id: str = GroupID.USER_GROUP.value
    value_deserializer: Any = lambda x: orjson.loads(x)
