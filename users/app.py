import asyncio

from fastapi import FastAPI, Depends

from configs import get_configs
from deps import user_collection
from kafka_service import KafkaService
from repositories import UserRepositories
from response_configuration import response_conf
from schemas import QueryParams
from services import Service

app = FastAPI(title='Users')

loop = asyncio.get_event_loop()

options = {
    'server': f'{get_configs().kafka_broker}',
    'repositories': UserRepositories(collection=user_collection),
    'topic': 'user',
}


@app.on_event('startup')
async def event_startup():
    loop.create_task(KafkaService(**options).consume())


@app.on_event('shutdown')
async def event_shutdown():
    await KafkaService(**options).stop_consume()


@app.get(**response_conf.get('count'))
async def get_count_of_users(query_params: QueryParams = Depends(QueryParams.as_query)):
    return await Service(repository=UserRepositories(collection=user_collection)) \
        .count_of_users(query_params=query_params)


@app.get(**response_conf.get('users'))
async def get_users(limit: int = 20, skip: int = 0):
    return await Service(repository=UserRepositories(collection=user_collection)) \
        .get_users(limit=limit, skip=skip)


@app.get(**response_conf.get('detail_user'))
async def get_user(user_id: int):
    return await Service(repository=UserRepositories(collection=user_collection)) \
        .get_user(user_id=user_id)
