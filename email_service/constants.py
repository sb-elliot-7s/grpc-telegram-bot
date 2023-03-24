from enum import Enum


class DataStore(str, Enum):
    S3 = 's3'


class GroupID(str, Enum):
    EMAIL_USER = 'email_user'


class Topic(str, Enum):
    EMAIL = 'send_email'
