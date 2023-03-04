import datetime

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    user_id: int = Field(alias='id')
    username: str
    first_name: str | None
    last_name: str | None
    date_created: datetime.datetime

    @property
    def to_dict(self): return self.dict()
