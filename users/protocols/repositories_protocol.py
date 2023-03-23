from abc import ABC, abstractmethod


class UserRepositoriesProtocol(ABC):
    @abstractmethod
    async def get_user(self, user_id: int):
        pass

    @abstractmethod
    async def get_users(self, limit: int = 20, skip: int = 0):
        pass

    @abstractmethod
    async def count_of_users(self, filters: dict, skip: int | None = None, limit: int | None = None):
        pass

    @abstractmethod
    async def save_user(self, user: dict): pass

    @abstractmethod
    async def change_email(self, user_id: int, email: str | None):
        pass
