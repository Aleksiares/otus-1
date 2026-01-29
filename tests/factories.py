import random

from uuid_extension import uuid7
from faker import Faker

from src.services import PasswordHashingService
from src.repositories.models import UserData
from src.types import Gender


fake = Faker("ru_RU")


def generate_user_data(
    password: str,
    password_hashing_service: PasswordHashingService,
) -> UserData:
    hashed_password = password_hashing_service(password)
    return UserData(
        id=uuid7(),
        password_hash=hashed_password.password_hash,
        salt=hashed_password.salt,
        first_name=fake.first_name(),
        second_name=fake.last_name(),
        gender=random.choice(list(Gender)),
        birthday=fake.date_of_birth(minimum_age=18, maximum_age=80),
        biography=fake.text(max_nb_chars=500),
        city=fake.city(),
    )
