from uuid import uuid4
from starlette.testclient import TestClient

from src.repositories import UsersRepository
from src.services import PasswordHashingService
from tests.factories import generate_user_data


async def test_happy_path(
    client: TestClient,
    users_repository: UsersRepository,
    password_hashing_service: PasswordHashingService,
) -> None:
    user_data = generate_user_data("any", password_hashing_service)
    await users_repository.register_user(user_data)

    response = client.get(
        url=f"/api/v1/user/get/{user_data.id}/",
    )

    assert (response.status_code, response.json()) == (
        200,
        {
            "first_name": user_data.first_name,
            "second_name": user_data.second_name,
            "gender": user_data.gender.value,
            "birthday": user_data.birthday.isoformat(),
            "biography": user_data.biography,
            "city": user_data.city,
        },
    )


async def test_not_found(client: TestClient) -> None:
    response = client.get(
        url=f"/api/v1/user/get/{uuid4()}/",
    )

    assert (response.status_code, response.json()) == (
        404,
        {"detail": "User not found"},
    )
