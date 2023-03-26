import asyncio

from constants import Topic
from kafka_service import KafkaService

if __name__ == '__main__':
    asyncio.run(KafkaService(topics=Topic.EMAIL.value).consume())
