from cheat_bot.di import di_container
from cheat_bot.presenter import error_handlers


class S3Storage:
    def __init__(self):
        self._source = di_container.repository_container.s3_system

    def post(self, file_binary: bytes, bucket_name: str, route: str) -> None:
        try:
            self._source.add(file_binary, bucket_name, route)
        except error_handlers.ClientS3exception:
            raise error_handlers.ClientS3exception()

    def get(self, academy_year: str, route: str) -> list[str]:
        try:
            return self._source.get(academy_year, route)
        except error_handlers.ClientS3exception:
            raise error_handlers.ClientS3exception()
