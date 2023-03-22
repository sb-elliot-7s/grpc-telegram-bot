from dataclasses import dataclass
from enum import Enum

import aiohttp

from protocols.api_protocol import APIServiceProtocol
from schemas import QueryParams


class RoutePaths(str, Enum):
    USERS = '/users'
    DETAIL = '/users/{user_id}'
    COUNT = '/users/count'


@dataclass
class APIService(APIServiceProtocol):
    base_url: str

    async def _aiohttp_process(self, path: str, **params):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f'{self.base_url}{path}', params=params, ssl=False) as response:
                match response.status:
                    case 200:
                        return await response.json()
                    case 404:
                        return None
                    case _:
                        print('error')

    async def get_users(self, limit: int, skip: int):
        params = QueryParams(limit=limit, skip=skip).dict(exclude_none=True)
        return await self._aiohttp_process(path=RoutePaths.USERS.value, **params)

    async def get_user(self, user_id: int):
        return await self._aiohttp_process(path=RoutePaths.DETAIL.value.format(user_id=user_id))

    async def count_of_users(self, query_params: QueryParams):
        return await self._aiohttp_process(path=RoutePaths.COUNT.value, **query_params.dict(exclude_none=True))
