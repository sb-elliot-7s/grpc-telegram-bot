import asyncio

from configs import get_configs
from deps import user_collection
from kafka_service import KafkaService
from repositories import UserRepositories

if __name__ == '__main__':
    service = KafkaService(
        server=f'{get_configs().kafka_broker}',
        repositories=UserRepositories(collection=user_collection)
    )
    asyncio.run(service.consume(topic='user'))
