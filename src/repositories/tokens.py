from uuid import UUID
from datetime import datetime, UTC

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import select

from src.repositories.tables import tokens_tables
from src.repositories.base import Query


class CreateTokenQuery(Query):
    async def __call__(self, token_id: UUID, user_id: UUID) -> UUID:
        async with self._engine.begin() as connection:
            query = tokens_tables.insert().values(
                id=token_id,
                user_id=user_id,
                created_at=datetime.now(UTC),
            )
            await connection.execute(query)

        return token_id


class GetTokensByUserIDQuery(Query):
    async def __call__(self, user_id: UUID) -> list[UUID]:
        async with self._engine.begin() as connection:
            query = select(tokens_tables.c.id).where(
                tokens_tables.c.user_id == user_id,
            )

            result = await connection.execute(query)

        return [row[0] for row in result.fetchall()]


class TokensRepository:
    def __init__(self, engine: AsyncEngine) -> None:
        self.create_token = CreateTokenQuery(engine)
        self.get_tokens_by_user_id = GetTokensByUserIDQuery(engine)
