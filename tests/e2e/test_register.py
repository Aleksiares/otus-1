import pytest

from uuid import UUID
from datetime import date
from starlette.testclient import TestClient

from src.repositories import UsersRepository
from src.services import PasswordHashingService


async def test_happy_path(
    client: TestClient,
    users_repository: UsersRepository,
    password_hashing_service: PasswordHashingService,
) -> None:
    response = client.post(
        url="/api/v1/user/register/",
        json={
            "password": "VeryHardPassword11@@",
            "first_name": "Евлампий",
            "second_name": "Стрыкало",
            "gender": "male",
            "birthday": "1990-01-01",
            "biography": "Что-то о себе",
            "city": "Эльдорадо",
        },
    )

    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    user_id = response_data["id"]
    user_data = await users_repository.get_user_by_user_id(user_id)
    assert user_data is not None
    assert user_data.id == UUID(user_id)
    assert user_data.first_name == "Евлампий"
    assert user_data.second_name == "Стрыкало"
    assert user_data.gender == "male"
    assert user_data.birthday == date(1990, 1, 1)
    assert user_data.biography == "Что-то о себе"
    assert user_data.city == "Эльдорадо"
    expected_password_hash = password_hashing_service(
        "VeryHardPassword11@@", user_data.salt
    )
    assert user_data.password_hash == expected_password_hash.password_hash


@pytest.mark.parametrize(
    "password",
    [
        pytest.param("veryhardpassword11@@", id="without_uppercase"),
        pytest.param("VERYHARDPASSWORD11@@", id="without_letters"),
        pytest.param("VeryHardPassword11", id="without_specials"),
        pytest.param("VeryHardPassword@@", id="without_numbers"),
    ],
)
def test_not_password_strength_error(password: str, client: TestClient) -> None:
    response = client.post(
        url="/api/v1/user/register/",
        json={
            "password": password,
            "first_name": "Евлампий",
            "second_name": "Стрыкало",
            "gender": "male",
            "birthday": "1990-01-01",
            "biography": "Что-то о себе",
            "city": "Эльдорадо",
        },
    )

    assert (response.status_code, response.json()) == (
        422,
        {
            "detail": [
                {
                    "type": "value_error",
                    "loc": ["body", "password"],
                    "msg": "Value error, Password must contain uppercase letters, lowercase characters, special characters, and numbers",
                    "input": password,
                    "ctx": {"error": {}},
                }
            ]
        },
    )


def test_short_length_password_error(client: TestClient) -> None:
    response = client.post(
        url="/api/v1/user/register/",
        json={
            "password": "Hard11@@@",
            "first_name": "Евлампий",
            "second_name": "Стрыкало",
            "gender": "male",
            "birthday": "1990-01-01",
            "biography": "Что-то о себе",
            "city": "Эльдорадо",
        },
    )

    assert (response.status_code, response.json()) == (
        422,
        {
            "detail": [
                {
                    "type": "string_too_short",
                    "loc": ["body", "password"],
                    "msg": "String should have at least 10 characters",
                    "input": "Hard11@@@",
                    "ctx": {"min_length": 10},
                }
            ]
        },
    )


def test_long_length_password_error(client: TestClient) -> None:
    response = client.post(
        url="/api/v1/user/register/",
        json={
            "password": "SuperVeryHardPassword11@@@",
            "first_name": "Евлампий",
            "second_name": "Стрыкало",
            "gender": "male",
            "birthday": "1990-01-01",
            "biography": "Что-то о себе",
            "city": "Эльдорадо",
        },
    )

    assert (response.status_code, response.json()) == (
        422,
        {
            "detail": [
                {
                    "type": "string_too_long",
                    "loc": ["body", "password"],
                    "msg": "String should have at most 25 characters",
                    "input": "SuperVeryHardPassword11@@@",
                    "ctx": {"max_length": 25},
                }
            ]
        },
    )
