from fastapi import FastAPI, HTTPException, status, Depends, responses
from pydantic import HttpUrl

from configs import get_configs
from response_options import response_conf
from schemas import QueryParams
from service import APIService

app = FastAPI(title='API', default_response_class=responses.ORJSONResponse)

url = HttpUrl(url=f'http://{get_configs().user_service_host}:8001', scheme='http')


@app.get(**response_conf.get('users'))
async def get_users(limit: int = 20, skip: int = 0):
    return await APIService(base_url=url).get_users(limit=limit, skip=skip)


@app.get(**response_conf.get('count'))
async def count_of_users(query_params: QueryParams = Depends(QueryParams.as_query)):
    return await APIService(base_url=url).count_of_users(query_params=query_params)


@app.get(**response_conf.get('detail_user'))
async def get_detail_user(user_id: int):
    if not (user := await APIService(base_url=url).get_user(user_id=user_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user
