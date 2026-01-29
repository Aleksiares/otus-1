from logging import Logger
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends

from src.api.models import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    GetUserResponse,
)
from src.dependencies import (
    get_users_repository,
    get_password_hashing_service,
    get_tokens_repository,
    get_ids_generator_service,
    get_logger,
)
from src.errors import NotFoundHTTPException
from src.repositories.models import UserData
from src.repositories import UsersRepository, TokensRepository
from src.services import IDsGenerationService, PasswordHashingService

api_router = APIRouter()


@api_router.post(path="/login/", response_model=LoginResponse)
async def login(
    request_data: LoginRequest,
    users_repository: Annotated[
        UsersRepository,
        Depends(get_users_repository),
    ],
    tokens_repository: Annotated[
        TokensRepository,
        Depends(get_tokens_repository),
    ],
    user_id_generation_service: Annotated[
        IDsGenerationService, Depends(get_ids_generator_service)
    ],
    password_hashing_service: Annotated[
        PasswordHashingService, Depends(get_password_hashing_service)
    ],
    logger: Annotated[
        Logger,
        Depends(get_logger),
    ],
) -> LoginResponse:
    logger.debug("Request to login", extra={"user_id": request_data.id})

    user_data = await users_repository.get_user_by_user_id(request_data.id)
    if user_data is None:
        logger.debug("User not found")
        raise NotFoundHTTPException()

    password_hashed_result = password_hashing_service(
        request_data.password, salt=user_data.salt
    )
    if user_data.password_hash != password_hashed_result.password_hash:
        logger.debug("Incorrect password")
        raise NotFoundHTTPException()

    token_id = user_id_generation_service.generate_token_id()
    await tokens_repository.create_token(token_id=token_id, user_id=user_data.id)

    return LoginResponse(token=str(token_id))


@api_router.post(path="/user/register/", response_model=RegisterResponse)
async def register_user(
    request_data: RegisterRequest,
    users_repository: Annotated[
        UsersRepository,
        Depends(get_users_repository),
    ],
    user_id_generation_service: Annotated[
        IDsGenerationService, Depends(get_ids_generator_service)
    ],
    password_hashing_service: Annotated[
        PasswordHashingService, Depends(get_password_hashing_service)
    ],
    logger: Annotated[
        Logger,
        Depends(get_logger),
    ],
) -> RegisterResponse:
    logger.debug(
        "Request to register", extra={**request_data.model_dump(exclude={"password"})}
    )

    user_id = user_id_generation_service.generate_user_id()
    password_hashed_result = password_hashing_service(request_data.password)
    register_data = UserData(
        id=user_id,
        password_hash=password_hashed_result.password_hash,
        salt=password_hashed_result.salt,
        first_name=request_data.first_name,
        second_name=request_data.second_name,
        gender=request_data.gender,
        birthday=request_data.birthday,
        biography=request_data.biography,
        city=request_data.city,
    )
    await users_repository.register_user(register_data)

    return RegisterResponse(id=user_id)


@api_router.get(path="/user/get/{user_id}/", response_model=GetUserResponse)
async def get_user_by_id(
    user_id: UUID,
    users_repository: Annotated[
        UsersRepository,
        Depends(get_users_repository),
    ],
    logger: Annotated[
        Logger,
        Depends(get_logger),
    ],
) -> GetUserResponse:
    logger.debug("Request to get a user by id", extra={"user_id": user_id})

    user_data = await users_repository.get_user_by_user_id(user_id)

    if user_data is None:
        raise NotFoundHTTPException()

    return GetUserResponse(
        first_name=user_data.first_name,
        second_name=user_data.second_name,
        gender=user_data.gender,
        birthday=user_data.birthday,
        biography=user_data.biography,
        city=user_data.city,
    )
