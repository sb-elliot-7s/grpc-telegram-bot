from fastapi import FastAPI, status

from deps import user_collection
from repositories import UserRepositories
from schemas import UserSchema

app = FastAPI()

response_conf = {
    'users': {
        'path': '/users',
        'status_code': status.HTTP_200_OK,
        'response_model': list[UserSchema],
        'response_model_by_alias': False
    },
    'detail': {
        'path': '/users/{user_id}',
        'status_code': status.HTTP_200_OK,
        'response_model': UserSchema,
        'response_model_by_alias': False
    },
    'count': {
        'path': '/users/count',
        'status_code': status.HTTP_200_OK,
        'response_model': int
    }
}


@app.get(**response_conf.get('users'))
async def get_users(limit: int = 20, skip: int = 0):
    repositories = UserRepositories(collection=user_collection)
    return await repositories.get_users(limit=limit, skip=skip)


@app.get(**response_conf.get('count'))
async def count_of_users(skip: int | None = None, limit: int | None = None):
    return await UserRepositories(collection=user_collection) \
        .count_of_users(filter_={}, skip=skip, limit=limit)


@app.get(**response_conf.get('detail'))
async def get_detail_user(user_id: int):
    repositories = UserRepositories(collection=user_collection)
    return await repositories.get_user(user_id=user_id)
