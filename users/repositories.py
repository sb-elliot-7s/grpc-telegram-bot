from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorCollection


@dataclass
class UserRepositories:
    collection: AsyncIOMotorCollection

    async def save_user(self, user: dict):
        _ = await self.collection.insert_one(document=user)

    async def get_user(self, user_id: int):
        return await self.collection.find_one({'_id': user_id})
