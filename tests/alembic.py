import os
from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace
from typing import (
    AsyncIterator,
)
from pydantic import PostgresDsn
from alembic.command import downgrade, upgrade
from alembic.config import Config


def make_alembic_config_from_url(postgres_dsn: str) -> Config:
    current_working_directory = Path.cwd().absolute()
    cmd_opts = SimpleNamespace(
        config=os.path.join(current_working_directory, "alembic.ini"),
        name="alembic",
        pg_url=postgres_dsn,
        raiseerr=False,
        x=None,
    )
    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts)  # type:ignore[arg-type]
    config.set_main_option(
        "script_location", os.path.join(current_working_directory, "migrations")
    )
    config.set_main_option("sqlalchemy.url", cmd_opts.pg_url)

    return config


@asynccontextmanager
async def alembic_migrator(postgres_dsn: PostgresDsn) -> AsyncIterator[None]:
    pycopg_postgres_dsn = str(postgres_dsn).replace(
        "postgresql://", "postgresql+psycopg://"
    )
    alembic_config = make_alembic_config_from_url(pycopg_postgres_dsn)
    upgrade(alembic_config, "head")
    yield
    downgrade(alembic_config, "base")
