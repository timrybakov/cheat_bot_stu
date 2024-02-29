from cheat_bot.repository.sources.s3_repository.s3_repository import S3Repository


class S3Interface:
    def __init__(self, s3_repository: S3Repository):
        self.__source = s3_repository

    def add(self, file_binary: bytes, bucket_name: str, route: str) -> None:
        self.__source.add(file_binary, bucket_name, route)

    def get(self, bucket_name: str, route: str, expiration: int = 360) -> list | None:
        return self.__source.get(bucket_name, route, expiration)
