from typing import Annotated

from logging import Logger
from loguru import logger
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from starlette.applications import State
from src.app.settings import Settings
from src.repositories import UsersRepository, TokensRepository
from src.services import PasswordHashingService, IDsGenerationService


async def get_state(request: Request) -> State:
    return request.app.state


async def get_settings(state: Annotated[State, Depends(get_state)]) -> Settings:
    return getattr(state, "settings")


async def get_database_engine(
    state: Annotated[State, Depends(get_state)],
) -> AsyncEngine:
    return getattr(state, "database_engine")


async def get_users_repository(request: Request) -> UsersRepository:
    state = await get_state(request)
    engine = await get_database_engine(state)
    return UsersRepository(engine)


async def get_tokens_repository(request: Request) -> TokensRepository:
    state = await get_state(request)
    engine = await get_database_engine(state)
    return TokensRepository(engine)


async def get_password_hashing_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> PasswordHashingService:
    return PasswordHashingService(settings.number_of_rounds_when_generating_salt)


async def get_ids_generator_service() -> IDsGenerationService:
    return IDsGenerationService()


async def get_logger() -> Logger:
    return logger  # type: ignore[return-value]
