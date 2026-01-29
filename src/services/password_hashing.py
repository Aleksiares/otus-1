from dataclasses import dataclass

import bcrypt


@dataclass
class PasswordHashResult:
    password_hash: str
    salt: bytes


class PasswordHashingService:
    def __init__(self, number_of_rounds_when_generating_salt: int) -> None:
        self._number_of_rounds_when_generating_salt = (
            number_of_rounds_when_generating_salt
        )

    def _generate_salt(self) -> bytes:
        return bcrypt.gensalt(rounds=self._number_of_rounds_when_generating_salt)

    def __call__(self, password: str, salt: bytes | None = None) -> PasswordHashResult:
        if salt is None:
            salt = self._generate_salt()

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return PasswordHashResult(
            password_hash=hashed_password.decode("utf-8"),
            salt=salt,
        )
