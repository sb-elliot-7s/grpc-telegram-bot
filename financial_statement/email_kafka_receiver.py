from dataclasses import dataclass

from aiokafka import AIOKafkaProducer

from configs import get_configs
from constants import Topic
from schemas import KafkaEmailPayloadSchema, KafkaSettingsSchema


@dataclass
class EmailKafkaReceiver:
    filename: str
    to_user: str | None
    link: str | None
    server: str = get_configs().kafka_broker
    topic: str = Topic.SEND_EMAIL.value

    async def produce_data(self):
        producer = AIOKafkaProducer(**KafkaSettingsSchema(bootstrap_servers=self.server).dict())
        await producer.start()
        try:
            payload = KafkaEmailPayloadSchema(filename=self.filename, to_user=self.to_user, link=self.link)
            await producer.send_and_wait(topic=self.topic, value=payload.dict())
        finally:
            await producer.stop()
