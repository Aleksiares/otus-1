from contextlib import asynccontextmanager
from typing import AsyncGenerator, AsyncIterator

from fastapi import FastAPI
from fastapi.applications import Lifespan, AppType
from pydantic import PostgresDsn
from sqlalchemy import make_url, URL
from sqlalchemy.ext.asyncio.engine import create_async_engine, AsyncEngine

from src.app.settings import Settings


def patch_dsn(dsn: PostgresDsn) -> URL:
    return make_url(str(dsn)).set(drivername="postgresql+psycopg_async")


@asynccontextmanager
async def create_sqlalchemy_engine(url: URL) -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(url=url, pool_pre_ping=True)
    try:
        yield engine
    finally:
        await engine.dispose()


def initialize_lifespan(
    settings: Settings,
) -> Lifespan[AppType]:
    @asynccontextmanager
    async def wrapper(app: FastAPI) -> AsyncGenerator[None]:
        state = getattr(app, "state")
        setattr(state, "settings", settings)

        async with create_sqlalchemy_engine(patch_dsn(settings.postgres_dsn)) as engine:
            setattr(state, "database_engine", engine)
            yield

    return wrapper
