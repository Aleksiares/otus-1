from dataclasses import dataclass
from datetime import date

from uuid import UUID

from src.types import Gender


@dataclass(frozen=True, slots=True)
class UserData:
    id: UUID
    password_hash: str
    salt: bytes
    first_name: str
    second_name: str
    gender: Gender
    birthday: date
    biography: str
    city: str
