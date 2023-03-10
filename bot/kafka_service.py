from dataclasses import dataclass

import orjson
from aiokafka import AIOKafkaProducer


@dataclass
class KafkaService:
    server: str

    async def produce(self, value: dict, topic: str):
        producer = AIOKafkaProducer(
            bootstrap_servers=self.server,
            value_serializer=lambda x: orjson.dumps(x)
        )
        await producer.start()
        try:
            await producer.send_and_wait(topic=topic, value=value)
        finally:
            await producer.stop()
