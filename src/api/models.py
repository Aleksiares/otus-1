from dataclasses import dataclass
from datetime import date

from uuid import UUID
from pydantic import BaseModel, Field, field_validator

from src import consts
from src.types import Gender


class LoginRequest(BaseModel):
    id: UUID
    password: str = Field(
        min_length=consts.MIN_PASSWORD_LENGTH,
        max_length=consts.MAX_PASSWORD_LENGTH,
    )


@dataclass
class LoginResponse:
    token: str


class RegisterRequest(BaseModel):
    password: str = Field(
        min_length=consts.MIN_PASSWORD_LENGTH,
        max_length=consts.MAX_PASSWORD_LENGTH,
    )
    first_name: str = Field(
        min_length=consts.MIN_FIRST_NAME_LENGTH,
        max_length=consts.MAX_FIRST_NAME_LENGTH,
    )
    second_name: str = Field(
        min_length=consts.MIN_SECOND_NAME_LENGTH,
        max_length=consts.MAX_SECOND_NAME_LENGTH,
    )
    gender: Gender
    birthday: date
    biography: str = Field(
        min_length=consts.MIN_BIOGRAPHY_LENGTH,
        max_length=consts.MAX_BIOGRAPHY_LENGTH,
    )
    city: str = Field(
        min_length=consts.MIN_CITY_LENGTH,
        max_length=consts.MAX_CITY_LENGTH,
    )

    @field_validator("password")
    def check_password_strength(cls, value: str) -> str:
        if not consts.PASSWORD_STRENGTH_REGEX.match(value):
            raise ValueError(
                "Password must contain uppercase letters, lowercase characters, special characters, and numbers"
            )

        return value


@dataclass
class RegisterResponse:
    id: UUID


@dataclass
class GetUserResponse:
    first_name: str
    second_name: str
    gender: Gender
    birthday: date
    biography: str
    city: str
