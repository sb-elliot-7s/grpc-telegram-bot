from datetime import datetime

from pydantic import BaseModel, Field

from utils import Int_Or_None, Str_Or_None


class UserSchema(BaseModel):
    user_id: int = Field(alias='_id')
    username: Str_Or_None
    first_name: Str_Or_None
    last_name: Str_Or_None
    date_created: datetime

    class Config:
        json_encoders = {datetime: lambda x: x.strftime('%Y:%m:%d %H:%M')}


class Options(BaseModel):
    skip: Int_Or_None
    limit: Int_Or_None
