from functools import lru_cache

from pydantic import BaseSettings


class Configs(BaseSettings):
    mongo_host: str
    mongo_port: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_configs() -> Configs:
    return Configs()
