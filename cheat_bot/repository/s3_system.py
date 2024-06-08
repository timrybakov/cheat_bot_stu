from .sources.file_repository import file_repository
from ..presenter import error_handlers


class S3System:
    def __init__(self, repository: file_repository.FileRepository) -> None:
        self._source = repository

    def add(self, file_binary: bytes, academy_year: str, route: str) -> None:
        try:
            self._source.add(file_binary, academy_year, route)
        except error_handlers.ClientS3exception:
            raise error_handlers.ClientS3exception()

    def get(self, academy_year: str, route: str) -> list[str]:
        try:
            return self._source.get(academy_year, route)
        except error_handlers.ClientS3exception:
            raise error_handlers.ClientS3exception()
