from functools import cached_property

from cheat_bot.repository.s3_interface import S3Interface
from cheat_bot.repository.sources.postgres.postgres_connector import PostgresConnector
from cheat_bot.repository.sources.postgres.user_interface.user_interface_postgres import UserInterfacePostgres
from cheat_bot.repository.sources.s3_repository.s3_repository import S3Repository
from cheat_bot.repository.user_interface import UserInterface
from cheat_bot.utils.singleton_meta import SingletonMeta


class RepositoryContainer(metaclass=SingletonMeta):
    def __init__(self, settings):
        self.__settings = settings

    @cached_property
    def postgres_connector(self):
        return PostgresConnector(
            username=self.__settings.DB_USER,
            password=self.__settings.DB_PASS,
            host=self.__settings.DB_HOST,
            db_name=self.__settings.DB_NAME
        )

    @cached_property
    def user_interface(self):
        return UserInterface(
            source=self.__user_interface_postgres
        )

    @cached_property
    def __user_interface_postgres(self):
        return UserInterfacePostgres(
            postgres_connector=self.postgres_connector
        )

    @property
    def __s3_repository(self):
        return S3Repository()

    @property
    def s3_interface(self):
        return S3Interface(
            s3_repository=self.__s3_repository
        )
