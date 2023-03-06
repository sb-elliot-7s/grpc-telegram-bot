import motor.motor_asyncio

from configs import get_configs

client = motor.motor_asyncio.AsyncIOMotorClient(f'mongodb://{get_configs().mongo_host}:{get_configs().mongo_port}')

database = client.database
