import logging
import uuid
import boto3
import requests

from botocore.exceptions import ClientError

from cheat_bot.presenter import error_handlers


class S3Connector:
    def __init__(self) -> None:
        self._client = boto3.client('s3')
        self._resource = boto3.resource('s3')

    def upload_fileobj(self, file_binary: bytes, bucket_name: str, key: str) -> None:
        try:
            self._client.head_object(Bucket=bucket_name, Key=f'{key}/')
            new_image_route = f'{key}/{uuid.uuid4()}.jpg'
            response = self._client.generate_presigned_post(
                bucket_name,
                new_image_route,
                ExpiresIn=360
            )
            files = {'file': (new_image_route, file_binary)}
            requests.post(response['url'], data=response['fields'], files=files)
        except ClientError as error:
            logging.error(error)
            raise error_handlers.ClientS3exception()

    def download_fileobj(self, bucket_name: str, key: str) -> list[str]:
        result_list = []
        try:
            bucket = self._resource.Bucket(bucket_name)
            for obj in bucket.objects.filter(Prefix=key):
                response = self._client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': bucket_name,
                        'Key': obj.key
                    },
                    ExpiresIn=360
                )
                result_list.append(response)
            return result_list[1:]
        except error_handlers.ClientS3exception:
            raise error_handlers.ClientS3exception()
