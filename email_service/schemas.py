from typing import Any

import orjson
from pydantic import BaseModel, Field

from configs import get_configs
from constants import GroupID


class EmailDataSchema(BaseModel):
    filename: str
    to_user: str
    link: str | None


class EmailSchema(EmailDataSchema):
    from_user: str = get_configs().from_user
    email_host: str = get_configs().email_host
    email_port: int = get_configs().email_port
    email_password: str = get_configs().email_password

    @classmethod
    def from_email_data_schema(cls, schema: EmailDataSchema) -> dict:
        return cls(filename=schema.filename, to_user=schema.to_user, link=schema.link).dict()


class S3SBucketKeySchema(BaseModel):
    bucket: str = Field(alias='Bucket')
    key: str = Field(alias='Key')


class YandexS3StorageOptionsSchema(BaseModel):
    service_name: str = 's3'
    aws_access_key_id: str = get_configs().aws_access_key_id
    aws_secret_access_key: str = get_configs().aws_secret_access_key
    region_name: str = 'ru-central1'
    endpoint_url: str = 'https://storage.yandexcloud.net'


class KafkaSettingsSchema(BaseModel):
    bootstrap_servers: str = get_configs().kafka_broker
    group_id: str = GroupID.EMAIL_USER.value
    value_deserializer: Any = lambda x: orjson.loads(x)
