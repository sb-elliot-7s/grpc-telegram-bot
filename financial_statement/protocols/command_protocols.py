from abc import ABC, abstractmethod
from dataclasses import dataclass


class Command(ABC):
    @abstractmethod
    async def execute(self):
        pass


@dataclass
class CommandDecoratorProtocol(Command):
    command: Command

    async def execute(self): pass
