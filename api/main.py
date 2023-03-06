from fastapi import FastAPI

from deps import user_collection
from repositories import UserRepositories
from response_options import response_conf
from utils import Int_Or_None

app = FastAPI(title='API')


@app.get(**response_conf.get('users'))
async def get_users(limit: int = 20, skip: int = 0):
    return await UserRepositories(collection=user_collection) \
        .get_users(limit=limit, skip=skip)


@app.get(**response_conf.get('count'))
async def count_of_users(skip: Int_Or_None = None, limit: Int_Or_None = None):
    return await UserRepositories(collection=user_collection) \
        .count_of_users(filter_={}, skip=skip, limit=limit)


@app.get(**response_conf.get('detail_user'))
async def get_detail_user(user_id: int):
    return await UserRepositories(collection=user_collection) \
        .get_user(user_id=user_id)
