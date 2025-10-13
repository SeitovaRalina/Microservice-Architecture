from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.schemas.user import UserCreate, UserLogin, UserUpdate
from src.core.utils.security import get_password_hash, verify_password
from src.core.errors.exceptions import ConflictException, ValidationException, UnauthorizedException

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    q = await db.execute(select(User).where(User.email == email))
    return q.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    q = await db.execute(select(User).where(User.username == username))
    return q.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    q = await db.execute(select(User).where(User.id == user_id))
    return q.scalar_one_or_none()

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    user_by_email = await get_user_by_email(db, user_in.email)
    if user_by_email:
        raise ConflictException("Пользователь с таким email уже существует")
    user_by_username = await get_user_by_username(db, user_in.username)
    if user_by_username:
        raise ConflictException("Пользователь с таким именем уже существует")
    user = User(
        email=user_in.email,
        username=user_in.username,
        password_hash=get_password_hash(user_in.password),
        bio=user_in.bio,
        image_url=user_in.image_url,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def authenticate_user(db: AsyncSession, user_login: UserLogin) -> Optional[User]:
    if not user_login.email or not user_login.password:
        raise ValidationException("Поля email и password обязательны")

    user = await get_user_by_email(db, user_login.email)
    verify = user and verify_password(user_login.password, user.password_hash)

    if not user or not verify or user.is_deleted:
        raise UnauthorizedException("Неверный email или пароль")
    return user

async def update_user(db: AsyncSession, user: User, user_in: UserUpdate) -> User:
    if user_in.email:
        user.email = user_in.email
    if user_in.username:
        user.username = user_in.username
    if user_in.password:
        user.password_hash = get_password_hash(user_in.password)
    if user_in.bio:
        user.bio = user_in.bio
    if user_in.image_url:
        user.image_url = user_in.image_url

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user: User) -> None:
    user.is_deleted = True
    user.deleted_at = datetime.now(timezone.utc)
    db.add(user)
    await db.commit()