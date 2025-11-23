from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.schemas.user import UserCreate, UserLogin, UserUpdate
from src.repositories.user_repository import UserRepository
from src.core.utils.security import get_password_hash, verify_password
from src.core.errors.exceptions import (
    ConflictException,
    UnauthorizedException,
    ValidationException,
)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def register(self, data: UserCreate) -> User:
        if await self.repo.get_by_email(data.email):
            raise ConflictException("Пользователь с таким email уже существует")

        if await self.repo.get_by_username(data.username):
            raise ConflictException("Пользователь с таким именем уже существует")

        user = User(
            email=data.email,
            username=data.username,
            password_hash=get_password_hash(data.password),
            bio=data.bio,
            image_url=data.image_url,
        )

        return await self.repo.create(user)

    async def authenticate(self, data: UserLogin) -> User:
        if not data.email or not data.password:
            raise ValidationException("Поля email и password обязательны")

        user = await self.repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise UnauthorizedException("Неверный email или пароль")

        if user.is_deleted:
            raise UnauthorizedException("Пользователь удалён")

        return user

    async def update_profile(self, current_user: User, data: UserUpdate) -> User:
        update_data = data.model_dump(exclude_unset=True)

        if "email" in update_data and update_data["email"] != current_user.email:
            if await self.repo.get_by_email(update_data["email"]):
                raise ConflictException("Этот email уже занят")
            current_user.email = update_data["email"]

        if "username" in update_data and update_data["username"] != current_user.username:
            if await self.repo.get_by_username(update_data["username"]):
                raise ConflictException("Это имя пользователя уже занято")
            current_user.username = update_data["username"]

        if "password" in update_data:
            current_user.password_hash = get_password_hash(update_data["password"])

        if "bio" in update_data:
            current_user.bio = update_data["bio"]

        if "image_url" in update_data:
            current_user.image_url = update_data["image_url"]

        return await self.repo.update(current_user)

    async def delete_account(self, user: User) -> None:
        await self.repo.soft_delete(user)
