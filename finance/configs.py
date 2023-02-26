from pydantic import BaseSettings


class Configs(BaseSettings):
    redis_host: str
    redis_port: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def get_configs() -> Configs:
    return Configs()