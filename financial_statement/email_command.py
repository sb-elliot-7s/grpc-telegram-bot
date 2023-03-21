from dataclasses import dataclass

from protocols.command_protocols import CommandDecoratorProtocol
from protocols.email_service_protocol import EmailServiceProtocol


@dataclass
class EmailGrpcCommand(CommandDecoratorProtocol):
    email_service: EmailServiceProtocol

    async def execute(self):
        await self.__send_email()
        return await self.command.execute()

    async def __send_email(self):
        await self.email_service.send_email()
