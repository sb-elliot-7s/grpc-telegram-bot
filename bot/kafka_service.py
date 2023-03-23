from dataclasses import dataclass

from aiokafka import AIOKafkaProducer

from schemas import KafkaSettingsSchema


@dataclass
class KafkaService:
    server: str

    async def produce(self, value: dict, topic: str):
        producer = AIOKafkaProducer(**KafkaSettingsSchema(bootstrap_servers=self.server).dict())
        await producer.start()
        try:
            await producer.send_and_wait(topic=topic, value=value)
        finally:
            await producer.stop()
