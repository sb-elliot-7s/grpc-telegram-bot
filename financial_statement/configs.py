from functools import lru_cache

from pydantic import BaseSettings


class Configs(BaseSettings):
    api_token: str
    base_url: str

    redis_host: str
    redis_port: int

    from_user: str
    email_host: str
    email_port: int
    email_password: str

    expires_in_boto3: int = 3600
    bucket_name: str
    aws_access_key_id: str
    aws_secret_access_key: str

    kafka_broker: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_configs() -> Configs: return Configs()
