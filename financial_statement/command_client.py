from dataclasses import dataclass

from protocols.command_protocols import Command


@dataclass
class CommandClient:
    command: Command

    async def process(self):
        return await self.command.execute()
