from fastapi import status

from schemas import UserSchema

response_conf = {
    'users': {
        'path': '/users',
        'status_code': status.HTTP_200_OK,
        'response_model': list[UserSchema],
        'response_model_by_alias': False
    },
    'detail_user': {
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
