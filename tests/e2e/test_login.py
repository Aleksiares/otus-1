from uuid import UUID, uuid7
from starlette.testclient import TestClient

from src.repositories import UsersRepository, TokensRepository
from src.services import PasswordHashingService
from tests.factories import generate_user_data


async def test_happy_path(
    client: TestClient,
    users_repository: UsersRepository,
    tokens_repository: TokensRepository,
    password_hashing_service: PasswordHashingService,
) -> None:
    password = "VeryHardPassword11@@"
    user_data = generate_user_data(password, password_hashing_service)
    await users_repository.register_user(user_data)

    response = client.post(
        url="/api/v1/login/",
        json={
            "id": str(user_data.id),
            "password": password,
        },
    )
    received_token = UUID(response.json()["token"])

    assert response.status_code == 200
    tokens = await tokens_repository.get_tokens_by_user_id(user_id=user_data.id)
    assert tokens == [received_token]


async def test_has_not_user(
    client: TestClient,
    tokens_repository: TokensRepository,
) -> None:
    user_id = uuid7()
    response = client.post(
        url="/api/v1/login/",
        json={
            "id": str(user_id),
            "password": "VeryHardPassword11@@",
        },
    )

    assert (response.status_code, response.json()) == (
        404,
        {"detail": "User not found"},
    )
    tokens = await tokens_repository.get_tokens_by_user_id(user_id=user_id)
    assert tokens == []


async def test_incorrect_password(
    client: TestClient,
    users_repository: UsersRepository,
    tokens_repository: TokensRepository,
    password_hashing_service: PasswordHashingService,
) -> None:
    user_data = generate_user_data("any", password_hashing_service)
    await users_repository.register_user(user_data)

    response = client.post(
        url="/api/v1/login/",
        json={
            "id": str(user_data.id),
            "password": "incorrect_password",
        },
    )

    assert (response.status_code, response.json()) == (
        404,
        {"detail": "User not found"},
    )
    tokens = await tokens_repository.get_tokens_by_user_id(user_id=user_data.id)
    assert tokens == []
