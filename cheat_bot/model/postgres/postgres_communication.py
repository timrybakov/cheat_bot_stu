from cheat_bot.di import di_container
from cheat_bot.presenter import error_handlers
from ..sсhemes.schemes import UserScheme


class PostgresCommunication:
    def __init__(self) -> None:
        self._source = di_container.repository_container.user_system

    async def create(self, data: UserScheme) -> None:
        try:
            await self._source.create(data)
        except error_handlers.NotUniqueException:
            raise error_handlers.NotUniqueException()

    async def select(self) -> UserScheme:
        try:
            return await self._source.get_first()
        except error_handlers.NoMaterialException:
            raise error_handlers.NoMaterialException()

    async def delete(self, obj: UserScheme) -> None:
        try:
            await self._source.delete(
                id_=obj.id
            )
        except error_handlers.NoMaterialException:
            raise error_handlers.NoMaterialException()
