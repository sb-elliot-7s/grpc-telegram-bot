from dataclasses import dataclass

from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection

from schemas import Options
from utils import Int_Or_None


@dataclass
class UserRepositories:
    collection: AsyncIOMotorCollection

    async def get_user(self, user_id: int) -> dict:
        if not (user := await self.collection.find_one(filter={'_id': user_id})):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {user_id} not found')
        return user

    async def get_users(self, limit: int, skip: int) -> list[dict]:
        return [user async for user in self.collection.find().skip(skip).limit(limit)]

    async def count_of_users(self, filter_: dict, skip: Int_Or_None, limit: Int_Or_None) -> int:
        return await self.collection \
            .count_documents(filter=filter_, **Options(skip=skip, limit=limit).dict(exclude_none=True))
