from abc import ABC, abstractmethod

from schemas import QueryParams


class APIServiceProtocol(ABC):
    @abstractmethod
    async def get_users(self, limit: int, skip: int):
        pass

    @abstractmethod
    async def get_user(self, user_id: int):
        pass

    @abstractmethod
    async def count_of_users(self, query_params: QueryParams):
        pass
