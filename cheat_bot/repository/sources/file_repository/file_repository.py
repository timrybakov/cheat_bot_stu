from cheat_bot.presenter import error_handlers
from cheat_bot import clients


class FileRepository:
    def __init__(self, s3_connector: clients.S3Connector) -> None:
        self._conn = s3_connector

    def add(self, file_binary: bytes, bucket_name: str, route: str) -> None:
        try:
            return self._conn.upload_fileobj(file_binary, bucket_name, route)
        except error_handlers.ClientS3exception:
            raise error_handlers.ClientS3exception()

    def get(self, bucket_name: str, route: str) -> list[str]:
        try:
            return self._conn.download_fileobj(bucket_name, route)
        except error_handlers.ClientS3exception:
            raise error_handlers.ClientS3exception()
