from app.core.errors import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User
from app.repositories.users import UserRepository


class AuthUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register(self, email: str, password: str) -> User:
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user is not None:
            raise UserAlreadyExistsError

        password_hash = hash_password(password)

        return await self.user_repository.create(
            email=email,
            password_hash=password_hash,
        )

    async def login(self, email: str, password: str) -> str:
        user = await self.user_repository.get_by_email(email)
        if user is None:
            raise InvalidCredentialsError

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError

        return create_access_token(subject=str(user.id))

    async def get_profile(self, user_id: int) -> User:
        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError

        return user
