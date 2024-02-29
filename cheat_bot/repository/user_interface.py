from databases.interfaces import Record

from cheat_bot.repository.sources.postgres.user_interface.user_interface_postgres import UserInterfacePostgres


class UserInterface:
    def __init__(self, source: UserInterfacePostgres):
        self.__source = source

    async def create(
            self, username: str, user_telegram_id: int,
            file_path: str, image_id: str, bucket: str,
            file_unique_id: str
    ) -> None:
        await self.__source.create(
            username,
            user_telegram_id,
            file_path, image_id,
            bucket, file_unique_id
        )

    async def get_first(self) -> Record | None:
        return await self.__source.get_first()

    async def delete(self, id_) -> None:
        await self.__source.delete(id_)
