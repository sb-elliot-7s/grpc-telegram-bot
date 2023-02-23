from pydantic import BaseSettings


class Configs(BaseSettings):
    mongo_host: str
    mongo_port: int
    kafka_broker: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def get_configs() -> Configs:
    return Configs()
