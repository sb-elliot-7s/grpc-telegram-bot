from enum import Enum


class GroupID(str, Enum):
    USER_GROUP = 'user-group'


class Topic(str, Enum):
    USER = 'user'
    SAVE_EMAIL = 'save_email'
    REMOVE_EMAIL = 'remove_email'
