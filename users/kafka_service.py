import json

from aiokafka import AIOKafkaConsumer

from repositories import UserRepositories
from schemas import UserSchema


class KafkaService:
    def __init__(self, repositories: UserRepositories, server: str, topic: str):
        self.repositories = repositories
        self.server: str
        self.topic = topic
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=server,
            group_id='user-group',
            value_deserializer=lambda x: json.loads(x)
        )

    async def consume(self):
        await self.consumer.start()
        try:
            async for message in self.consumer:
                if not await self.repositories.get_user(user_id=message.value.get('user_id')):
                    user = UserSchema(**message.value)
                    await self.repositories.save_user(user=user.to_mongo_obj())
        finally:
            await self.consumer.stop()

    async def stop_consume(self):
        await self.consumer.stop()
