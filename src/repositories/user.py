from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncEngine
from dataclasses import asdict

from src.repositories.tables import users_tables
from src.repositories.base import Query
from src.repositories.models import UserData


class RegisterUserQuery(Query):
    async def __call__(self, user_data: UserData) -> None:
        async with self._engine.begin() as connection:
            query = users_tables.insert().values(**asdict(user_data))
            await connection.execute(query)


class GetByUserID(Query):
    async def __call__(self, user_id: UUID) -> UserData | None:
        query = (
            users_tables.select()
            .where(
                users_tables.c.id == user_id,
            )
            .limit(1)
        )

        async with self._engine.begin() as connection:
            result = await connection.execute(query)

        row_data = result.mappings().first()

        return UserData(**row_data) if row_data else None


class UsersRepository:
    def __init__(self, engine: AsyncEngine) -> None:
        self.register_user = RegisterUserQuery(engine)
        self.get_user_by_user_id = GetByUserID(engine)
