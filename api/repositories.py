from dataclasses import dataclass

from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection


@dataclass
class UserRepositories:
    collection: AsyncIOMotorCollection

    async def get_user(self, user_id: int) -> dict:
        if not (user := await self.collection.find_one(filter={'_id': user_id})):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
        return user

    async def get_users(self, limit: int, skip: int) -> list[dict]:
        cursor = self.collection.find().skip(skip).limit(limit)
        return [user async for user in cursor]
