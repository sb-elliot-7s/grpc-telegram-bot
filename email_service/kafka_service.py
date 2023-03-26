import asyncio
from dataclasses import dataclass

from aiokafka import AIOKafkaConsumer

from configs import get_configs
from constants import DataStore
from file_service import FileLoadService
from protocols.file_service_protocol import FSProtocol
from schemas import EmailDataSchema, EmailSchema, KafkaSettingsSchema
from service import EmailService


async def file_service_factory(store: DataStore) -> FSProtocol:
    match store:
        case DataStore.S3: return FileLoadService()


@dataclass
class KafkaService:
    topics: str | list[str]
    server: str = get_configs().kafka_broker

    async def consume(self):
        consumer = AIOKafkaConsumer(self.topics, **KafkaSettingsSchema(bootstrap_servers=self.server).dict())
        await consumer.start()
        try:
            async for msg in consumer:
                schema = EmailDataSchema(**msg.value)
                fs = await file_service_factory(store=DataStore.S3)
                pdf = await fs.download_pdf_file(filename=schema.filename)
                es = EmailService(pdf=pdf if pdf is not None else None, email_schema=EmailSchema(**schema.dict()))
                async with asyncio.TaskGroup() as tg:
                    tg.create_task(es.send_email())
        finally:
            await consumer.stop()
