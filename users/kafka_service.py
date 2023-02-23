import json
from dataclasses import dataclass

from aiokafka import AIOKafkaConsumer

from repositories import UserRepositories
from schemas import UserSchema


@dataclass
class KafkaService:
    repositories: UserRepositories
    server: str

    async def consume(self, topic: str):
        consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=self.server,
            group_id='user-group',
            value_deserializer=lambda x: json.loads(x)
        )
        await consumer.start()
        try:
            async for message in consumer:
                if not await self.repositories.get_user(user_id=message.value.get('user_id')):
                    user = UserSchema(**message.value)
                    await self.repositories.save_user(user=user.to_mongo_obj())
        finally:
            await consumer.stop()
