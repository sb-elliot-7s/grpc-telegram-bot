from dataclasses import dataclass

from email_kafka_receiver import EmailKafkaReceiver
from protocols.command_protocols import CommandDecoratorProtocol


@dataclass
class EmailKafkaCommand(CommandDecoratorProtocol):
    receiver: EmailKafkaReceiver

    async def execute(self):
        await self.__produce()
        return await self.command.execute()

    async def __produce(self):
        await self.receiver.produce_data()
