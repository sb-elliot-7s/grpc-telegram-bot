from functools import lru_cache

from pydantic import BaseSettings


class Configs(BaseSettings):
    from_user: str
    email_host: str
    email_port: int
    email_password: str

    kafka_broker: str

    bucket_name: str
    aws_access_key_id: str
    aws_secret_access_key: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_configs() -> Configs: return Configs()
