from abc import ABC, abstractmethod


class GRPCServiceProtocol(ABC):
    @abstractmethod
    async def response(self): pass
