from databases.interfaces import Record

from .sources.user_system.user_system_postgres import UserSystemPostgres
from cheat_bot.model import sсhemes
from ..presenter import error_handlers


class UserSystem:
    def __init__(self, source: UserSystemPostgres) -> None:
        self._source = source

    async def create(
        self,
        user_material: sсhemes.UserScheme
    ) -> None:
        try:
            await self._source.create(user_material)
        except error_handlers.NotUniqueException:
            raise error_handlers.NotUniqueException()

    async def get_first(self) -> Record | None:
        try:
            return await self._source.get_first()
        except error_handlers.NoMaterialException:
            raise error_handlers.NoMaterialException()

    async def delete(self, id_) -> None:
        try:
            await self._source.delete(id_)
        except error_handlers.NoMaterialException:
            raise error_handlers.NoMaterialException()
