from typing import Any

import orjson
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


class KafkaSettingsSchema(BaseModel):
    bootstrap_servers: list | str
    value_serializer: Any = lambda x: orjson.dumps(x)
    compression_type: str = 'gzip'


class KafkaEmailPayloadSchema(BaseModel):
    filename: str
    to_user: str | None
    link: str | None


class FilenameSchema(BaseModel):
    symbol: str
    year: str

    @property
    def filename(self):
        return f'{self.symbol}:{self.year}'


class PrintOptionsSchema(BaseModel):
    paperWidth: float
    paperHeight: float


class S3SBucketKeySchema(BaseModel):
    Bucket: str
    Key: str


class YandexS3StorageOptionsSchema(BaseModel):
    service_name: str = 's3'
    aws_access_key_id: str = get_configs().aws_access_key_id
    aws_secret_access_key: str = get_configs().aws_secret_access_key
    region_name: str = 'ru-central1'
    endpoint_url: str = 'https://storage.yandexcloud.net'
