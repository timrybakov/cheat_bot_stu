from databases.interfaces import Record

from .queries import (
    CREATE_USER_MATERIAL_QUERY,
    FETCH_FIRST_QUERY,
    DELETE_USER_MATERIAL_QUERY
)
from ..postgres_connector import PostgresConnector


class UserInterfacePostgres:
    def __init__(self, postgres_connector: PostgresConnector):
        self.__conn = postgres_connector

    async def create(
            self, username: str, user_telegram_id: int, file_path: str,
            image_id: str, bucket: str, file_unique_id: str
    ) -> None:
        await self.__conn.execute(
            CREATE_USER_MATERIAL_QUERY,
            values={
                'username': username,
                'user_telegram_id': user_telegram_id,
                'file_path': file_path,
                'image_id': image_id,
                'bucket': bucket,
                'file_unique_id': file_unique_id
            }
        )

    async def get_first(self) -> Record | None:
        return await self.__conn.fetch_one(FETCH_FIRST_QUERY, values=None)

    async def delete(self, id_: int) -> None:
        await self.__conn.execute(
            DELETE_USER_MATERIAL_QUERY,
            values={
                'id': id_
            }
        )
