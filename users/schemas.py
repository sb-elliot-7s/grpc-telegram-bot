from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    user_id: int
    username: str
    first_name: str | None
    last_name: str | None
    date_created: datetime

    class Config:
        json_encoders = {
            datetime: lambda x: x.strftime('%Y:%m:%d %H:%M')
        }

    def to_mongo_obj(self):
        return {
            '_id': self.user_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_created': self.date_created
        }
