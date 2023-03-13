from enum import Enum
from functools import lru_cache

from pydantic import BaseSettings


class Topic(str, Enum):
    USER = 'user'
    SAVE_EMAIL = 'save_email'


class Configs(BaseSettings):
    mongo_host: str
    mongo_port: int
    kafka_broker: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_configs() -> Configs:
    return Configs()
