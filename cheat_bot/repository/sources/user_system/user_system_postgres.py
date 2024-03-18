from asyncpg import UniqueViolationError

from cheat_bot.presenter import error_handlers
from . import queries
from cheat_bot import clients
from cheat_bot.model import sсhemes, database


class UserSystemPostgres:
    def __init__(self, postgres_connector: clients.PostgresConnector) -> None:
        self._conn = postgres_connector

    async def create(
        self,
        user_material: sсhemes.UserScheme
    ) -> None:
        try:
            await self._conn.execute(
                queries.CREATE_USER_MATERIAL_QUERY,
                values={
                    **user_material.model_dump()
                }
            )
        except UniqueViolationError:
            raise error_handlers.NotUniqueException

    async def get_first(self) -> database.User | None:
        try:
            return await self._conn.fetch_one(
                queries.FETCH_FIRST_QUERY,
                values=None
            )
        except AttributeError:
            raise error_handlers.NoMaterialException()

    async def delete(self, id_: int) -> None:
        try:
            await self._conn.execute(
                queries.DELETE_USER_MATERIAL_QUERY,
                values={
                    'id': id_
                }
            )
        except AttributeError:
            raise error_handlers.NoMaterialException()
