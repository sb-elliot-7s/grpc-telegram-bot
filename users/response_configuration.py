from typing import Any

from fastapi import status

from schemas import UserSchema


def get_common_options(
        *, status_code: int = status.HTTP_200_OK,
        model: Any,
        path: str = ''
) -> dict:
    return {
        'status_code': status_code,
        'response_model': model,
        'path': f'/users{path}',
    }


response_conf = {
    'users': {**get_common_options(model=list[UserSchema])},
    'detail_user': {**get_common_options(model=UserSchema, path='/{user_id}')},
    'count': {**get_common_options(model=int, path='/count')}
}
