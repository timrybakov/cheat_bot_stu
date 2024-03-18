from databases import Database
from databases.interfaces import Record


class PostgresConnector:
    def __init__(self, username: str, password: str, host: str, db_name: str) -> None:
        self.__db = Database(
            f"postgres://{username}:{password}@{host}/{db_name}"
        )

    async def execute(self, query: str, values: dict) -> Record | None:
        try:
            async with self.__db as db:
                return await db.execute(query=query, values=values)
        except AttributeError:
            raise AttributeError

    async def fetch_one(self, query: str, values: dict) -> Record | None:
        try:
            async with self.__db as db:
                return await db.fetch_one(query=query, values=values)
        except AttributeError:
            raise AttributeError
