from typing import (
    AsyncGenerator,
    Generator,
    Iterator,
    Any,
)
import pytest
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine
from testcontainers.postgres import PostgresContainer
from fastapi.testclient import TestClient

from src.app.runner import create_app
from src.app.settings import Settings
from src.repositories import TokensRepository, UsersRepository
from src.services import PasswordHashingService
from tests.alembic import alembic_migrator


_PG_CONTAINER = PostgresContainer(image="postgres:15", driver="psycopg")


@pytest.fixture(scope="session")
def postgres_container(request: pytest.FixtureRequest) -> Iterator[PostgresContainer]:
    with _PG_CONTAINER as container:
        yield container


@pytest.fixture(scope="session")
def postgres_dsn(postgres_container) -> str:
    return postgres_container.get_connection_url().replace("+psycopg", "")


@pytest.fixture(scope="session")
def settings(postgres_dsn: str) -> Settings:
    return Settings(postgres_dsn=postgres_dsn)


@pytest.fixture(scope="session")
async def app(settings: Settings) -> AsyncGenerator[FastAPI, Any]:
    async with alembic_migrator(settings.postgres_dsn):
        yield create_app(settings)


@pytest.fixture(scope="function")
def client(app: FastAPI) -> Generator[TestClient, None, None]:
    with TestClient(app) as client_:
        yield client_


@pytest.fixture(scope="function")
async def engine(app: FastAPI) -> AsyncGenerator[AsyncEngine, Any]:
    assert hasattr(app, "state")
    assert hasattr(app.state, "database_engine")
    assert isinstance(app.state.database_engine, AsyncEngine)
    yield getattr(app.state, "database_engine")


@pytest.fixture(scope="function")
def tokens_repository(engine: AsyncEngine) -> TokensRepository:
    return TokensRepository(engine)


@pytest.fixture(scope="function")
def users_repository(engine: AsyncEngine) -> UsersRepository:
    return UsersRepository(engine)


@pytest.fixture(scope="function")
def password_hashing_service() -> PasswordHashingService:
    return PasswordHashingService(number_of_rounds_when_generating_salt=10)
