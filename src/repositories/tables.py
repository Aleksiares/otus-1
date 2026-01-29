from sqlalchemy import Table, Column, String, Date, DateTime, Enum
from sqlalchemy.schema import MetaData
from sqlalchemy.dialects import postgresql

from src import consts
from src.types import Gender


metadata = MetaData()


users_tables = Table(
    "users",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True)),
    Column("password_hash", String()),
    Column("salt", postgresql.BYTEA()),
    Column("first_name", String(consts.MAX_FIRST_NAME_LENGTH)),
    Column("second_name", String(consts.MAX_SECOND_NAME_LENGTH)),
    Column("gender", Enum(Gender)),
    Column("birthday", Date()),
    Column("biography", String(consts.MAX_BIOGRAPHY_LENGTH)),
    Column("city", String(consts.MAX_CITY_LENGTH)),
)


tokens_tables = Table(
    "tokens",
    metadata,
    Column("id", postgresql.UUID(as_uuid=True)),
    Column(
        "user_id",
        postgresql.UUID(as_uuid=True),
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
    ),
)
