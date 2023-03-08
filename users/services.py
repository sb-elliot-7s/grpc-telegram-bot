from dataclasses import dataclass
from datetime import datetime

from fastapi import HTTPException, status

from protocols.repositories_protocol import UserRepositoriesProtocol
from schemas import QueryParams


@dataclass
class Service:
    repository: UserRepositoriesProtocol

    async def get_users(self, limit: int = 20, skip: int = 0):
        return await self.repository.get_users(limit=limit, skip=skip)

    async def count_of_users(self, query_params: QueryParams):
        operator = query_params.operator_date_created
        datetime_ = query_params.date_created
        filters = {
            'date_created': {f'${operator}': datetime.strptime(datetime_, '%Y-%m-%d %H:%M:%S')}} \
            if operator and datetime_ else {}
        return await self.repository.count_of_users(filters=filters, skip=query_params.skip, limit=query_params.limit)

    async def save_user(self, user: dict):
        return await self.repository.save_user(user=user)

    async def get_user(self, user_id: int):
        if not (user := await self.repository.get_user(user_id=user_id)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        return user
