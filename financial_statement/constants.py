from enum import Enum, IntEnum


class Topic(str, Enum):
    SEND_EMAIL = 'send_email'


class PDFGeneratorType(str, Enum):
    SELENIUM = 'selenium'


class TypePDFResponse(IntEnum):
    PDF_URL = 0
    PDF_BYTES = 1


class PDFStore(str, Enum):
    S3 = 's3'
    LOCAL = 'local'


class TypeFileReturned(str, Enum):
    FILE = 'file'
    URL = 'url'
