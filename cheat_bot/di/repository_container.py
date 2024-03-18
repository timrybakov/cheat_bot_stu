from functools import cached_property

from cheat_bot import repository, clients


class RepositoryContainer:
    def __init__(self, settings) -> None:
        self._settings = settings

    @cached_property
    def postgres_connector(self) -> clients.PostgresConnector:
        return clients.PostgresConnector(
            username=self._settings.db_settings.db_user,
            password=self._settings.db_settings.db_pass,
            host=self._settings.db_settings.db_host,
            db_name=self._settings.db_settings.db_name
        )

    @cached_property
    def user_system(self) -> repository.UserSystem:
        return repository.UserSystem(
            source=self._user_system_postgres
        )

    @cached_property
    def _user_system_postgres(self) -> repository.UserSystemPostgres:
        return repository.UserSystemPostgres(
            postgres_connector=self.postgres_connector
        )

    @property
    def _s3_repository(self) -> repository.FileRepository:
        return repository.FileRepository(
            s3_connector=self._s3_connector
        )

    @property
    def _s3_connector(self) -> clients.S3Connector:
        return clients.S3Connector()

    @property
    def s3_system(self) -> repository.S3System:
        return repository.S3System(
            repository=self._s3_repository
        )
