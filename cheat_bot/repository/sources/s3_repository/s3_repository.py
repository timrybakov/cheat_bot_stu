import logging

import boto3
import requests
import secrets
from botocore.exceptions import ClientError

from cheat_bot.config.config import settings
from .utils import BucketAccess

URI_INFO = f'https://api.telegram.org/bot{settings.AUTH_TOKEN}/getFile?file_id='
URI = f'https://api.telegram.org/file/bot{settings.AUTH_TOKEN}/'


class S3Repository:
    def __init__(self):
        self.client = boto3.client('s3')
        self.resource = boto3.resource('s3')

    def add(self, file_binary: bytes, bucket_name: str, route: str) -> None:
        self.client.head_object(Bucket=bucket_name, Key=f'{route}/')
        new_image_route = f'{route}/{secrets.token_hex(8)}.jpg'
        response = BucketAccess.create_presigned_post_url(
            client=self.client,
            bucket_name=bucket_name,
            object_name=new_image_route
        )
        files = {'file': (new_image_route, file_binary)}
        requests.post(response['url'], data=response['fields'], files=files)

    def get(self, bucket_name: str, route: str, expiration: int = 360) -> list | None:
        result_list = []
        bucket = self.resource.Bucket(bucket_name)
        try:
            for obj in bucket.objects.filter(Prefix=route):
                response = self.client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': bucket_name,
                        'Key': obj.key
                    },
                    ExpiresIn=expiration
                )
                result_list.append(response)
        except ClientError as error:
            logging.error(error)
            return None
        return result_list[1:]
