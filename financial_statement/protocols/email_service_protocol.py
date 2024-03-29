from abc import ABC, abstractmethod


class EmailServiceProtocol(ABC):
    @abstractmethod
    async def send_email(self): pass
