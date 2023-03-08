from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorCollection

from protocols.repositories_protocol import UserRepositoriesProtocol
from schemas import Options, UserSchema


@dataclass
class UserRepositories(UserRepositoriesProtocol):
    collection: AsyncIOMotorCollection

    async def get_users(self, limit: int = 20, skip: int = 0):
        return [
            UserSchema.from_mongo_obj(user) async for user in self.collection
            .find()
            .skip(skip)
            .limit(limit)
        ]

    async def count_of_users(self, filters: dict, skip: int | None = None, limit: int | None = None):
        return await self.collection \
            .count_documents(filter=filters, **Options(skip=skip, limit=limit).dict(exclude_none=True))

    async def save_user(self, user: dict):
        _ = await self.collection.insert_one(document=user)

    async def get_user(self, user_id: int):
        user = await self.collection.find_one({'_id': user_id})
        return UserSchema.from_mongo_obj(mongo_user=user) if user else None
