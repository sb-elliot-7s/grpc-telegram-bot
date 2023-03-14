from dataclasses import dataclass

from protocols.command_protocols import Command
from protocols.grpc_service_protocol import GRPCServiceProtocol


@dataclass
class GRPCCommand(Command):
    receiver: GRPCServiceProtocol

    async def execute(self):
        return await self.receiver.response()
