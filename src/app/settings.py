from pydantic import PostgresDsn, PositiveInt
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    number_of_rounds_when_generating_salt: PositiveInt = 10
    postgres_dsn: PostgresDsn

    class Config:
        env_file = "local.env"
