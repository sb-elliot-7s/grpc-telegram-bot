import logging

import orjson
from aiokafka import AIOKafkaConsumer

from configs import Topic
from repositories import UserRepositories
from schemas import UserSchema, UserUpdateSchema

logging.basicConfig(level=logging.DEBUG, filename='k.log')


class KafkaService:
    def __init__(self, repositories: UserRepositories, server: str, topic: list[str]):
        self.repositories = repositories
        self.server: str
        self.topic = topic
        self.consumer = AIOKafkaConsumer(
            *self.topic,
            bootstrap_servers=server,
            group_id='user-group',
            value_deserializer=lambda x: orjson.loads(x)
        )

    async def __handle_user_topic(self, message):
        if not await self.repositories.get_user(user_id=message.value.get('user_id')):
            user = UserSchema(**message.value)
            await self.repositories.save_user(user=user.to_mongo_obj())

    async def __handle_update_email_topic(self, message):
        user_email = UserUpdateSchema(**message.value)
        await self.repositories.update_user(user_data=user_email)

    async def __handle_remove_email(self, message):
        await self.repositories.remove_email(user_id=message.value['user_id'])

    async def _handle_messages(self, message):
        match message.topic:
            case Topic.SAVE_EMAIL.value:
                await self.__handle_update_email_topic(message=message)
            case Topic.USER.value:
                await self.__handle_user_topic(message=message)
            case Topic.REMOVE_EMAIL.value:
                await self.__handle_remove_email(message=message)

    async def consume(self):
        await self.consumer.start()
        try:
            async for message in self.consumer:
                logging.debug('MESAGE: %s', message.value)
                await self._handle_messages(message=message)
        finally:
            await self.consumer.stop()

    async def stop_consume(self):
        await self.consumer.stop()
