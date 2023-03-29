import asyncio
import gzip
import io

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from configs import get_configs
from constants import TypeFileReturned
from protocols.file_service_protocol import FileProtocol
from schemas import S3SBucketKeySchema, YandexS3StorageOptionsSchema


class S3StorageFileService(FileProtocol):

    def __init__(self, bucket: str = get_configs().bucket_name,
                 type_file_returned: TypeFileReturned = TypeFileReturned.URL):
        self.__bucket = bucket
        self.__session = boto3.session.Session()
        self.__s3: BaseClient = self.__session.client(**YandexS3StorageOptionsSchema().dict())
        self.__type_file_returned = type_file_returned
        self.__params: dict | None = None

    async def download_pdf(self, filename: str) -> str | bytes:
        match self.__type_file_returned:
            case TypeFileReturned.FILE:
                return gzip.compress(await self.__get_object(filename=filename))
            case TypeFileReturned.URL:
                return await self.__generate_url(filename=filename)

    async def save_pdf(self, filename: str, pdf: bytes):
        await asyncio.to_thread(self.__s3.upload_fileobj, Fileobj=io.BytesIO(pdf),
                                **self.__prepare_bucket_and_key(filename=filename))

    async def delete_pdf(self, filename: str):
        await asyncio.to_thread(self.__s3.delete_objects, **self.__prepare_bucket_and_key(filename=filename))

    async def is_file_exist(self, filename: str) -> bool:
        try:
            _ = await asyncio.to_thread(self.__s3.head_object, **self.__prepare_bucket_and_key(filename=filename))
            return True
        except ClientError:
            return False

    def __prepare_bucket_and_key(self, filename: str) -> dict:
        return S3SBucketKeySchema(Bucket=self.__bucket, Key=f'reports/{filename}.pdf').dict(by_alias=True)

    async def __generate_url(self, filename: str) -> str:
        return await asyncio.to_thread(self.__s3.generate_presigned_url, ClientMethod='get_object',
                                       Params=self.__prepare_bucket_and_key(filename=filename),
                                       ExpiresIn=get_configs().expires_in_boto3)

    def set_extra_params(self, **kwargs):
        """optional to add params in get_object method"""
        self.__params = kwargs
        return self

    async def __get_object(self, filename: str) -> bytes:
        options = self.__prepare_bucket_and_key(filename=filename)
        if self.__params:
            options.update(**self.__params)
        result = await asyncio.to_thread(self.__s3.get_object, **options)
        return result['Body'].read()
