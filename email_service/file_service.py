import asyncio

import boto3

from configs import get_configs
from protocols.file_service_protocol import FSProtocol
from schemas import S3SBucketKeySchema, YandexS3StorageOptionsSchema


class FileLoadService(FSProtocol):
    def __init__(self, bucket: str = get_configs().bucket_name):
        self.session = boto3.session.Session()
        self.__s3 = self.session.client(**YandexS3StorageOptionsSchema().dict())
        self.__bucket = bucket

    async def download_pdf_file(self, filename: str):
        schema = S3SBucketKeySchema(Bucket=self.__bucket, Key=f'reports/{filename}.pdf')
        try:
            result = await asyncio.to_thread(self.__s3.get_object, **schema.dict(by_alias=True))
            return result['Body'].read()
        except self.__s3.exceptions.NoSuchKey:
            return None
