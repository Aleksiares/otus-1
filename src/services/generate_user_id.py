from uuid import UUID
from uuid_extension import uuid7


class IDsGenerationService:
    @staticmethod
    def generate_user_id() -> UUID:
        return uuid7()

    @staticmethod
    def generate_token_id() -> UUID:
        return uuid7()
