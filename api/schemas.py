from datetime import datetime

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    user_id: int = Field(alias='_id')
    username: str
    first_name: str | None
    last_name: str | None
    date_created: datetime

    class Config:
        json_encoders = {
            datetime: lambda x: x.strftime('%Y:%m:%d %H:%M')
        }


class Options(BaseModel):
    skip: int | None
    limit: int | None
