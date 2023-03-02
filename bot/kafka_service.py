import json
from dataclasses import dataclass

from aiokafka import AIOKafkaProducer


@dataclass
class KafkaService:
    server: str

    async def produce(self, value: dict, topic: str):
        producer = AIOKafkaProducer(
            bootstrap_servers=self.server,
            value_serializer=lambda x: json.dumps(x, default=str).encode('utf-8')
        )
        await producer.start()
        try:
            await producer.send_and_wait(topic=topic, value=value)
        finally:
            await producer.stop()
