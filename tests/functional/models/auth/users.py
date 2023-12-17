"""Модель данных пользователя."""
import uuid
from datetime import datetime
from typing import ClassVar

from passlib.context import CryptContext  # passlib рекомендована к использованию
# в проектном задании 6-го спринта.
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship

from tests.functional import settings
from tests.functional.models.auth.base import Base

pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto',
)


class User(Base):
    """Модель данных пользователя."""

    __tablename__ = 'users'

    id: ClassVar = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    email: ClassVar = Column(
        String(settings.standard_char_field_len),
        unique=True,
        nullable=False,
    )
    password: ClassVar = Column(String(settings.long_char_field_len), nullable=False)
    first_name: ClassVar = Column(String(settings.standard_char_field_len))
    last_name: ClassVar = Column(String(settings.standard_char_field_len))
    disabled: ClassVar = Column(Boolean, default=False)
    created_at: ClassVar = Column(DateTime, default=datetime.utcnow)

    third_party_users: Mapped['ThirdPartyUser'] = relationship(back_populates='users')
    users_histories: Mapped['UsersHistory'] = relationship(back_populates='users')

    def __init__(  # noqa: WPS211 у метода слишком много параметров (но здесь все они необходимы)
        self,
        email: str,
        password: str,
        first_name: str = '',
        last_name: str = '',
        disabled: bool = False,
    ) -> None:
        """Инициализация записи пользователя.

        Args:
            email: адрес электронной почты пользователя,
            password: пароль пользователя,
            first_name: имя пользователя,
            last_name: фамилия пользователя,
            disabled: отключен ли пользователь,
        """
        self.email = email  # noqa: WPS601 переопределяем атрибуты классы (это здесь необходимо)
        self.password = pwd_context.hash(password)  # noqa: WPS601
        self.first_name = first_name  # noqa: WPS601
        self.last_name = last_name  # noqa: WPS601
        self.disabled = disabled  # noqa: WPS601

    def __repr__(self) -> str:
        """Текстовое представление записи таблицы пользователей.

        Returns:
            строка, содержащая полное имя пользователя и его email.
        """
        return '<User {first_name} {last_name} with {email}>'.format(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
        )


class UserRole(Base):
    """Модель, реализующая связь многие ко многим между пользователями и их ролями."""

    __tablename__ = 'users_roles'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = Column(
        UUID,
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    role_id = Column(
        UUID,
        ForeignKey('roles.id', ondelete='CASCADE'),
        nullable=False,
    )
    user_role_idx = UniqueConstraint('user_id', 'role_id')

    def __init__(self, user_id: UUID, role_id: UUID) -> None:
        """Инициализация записи роли.

        Args:
            user_id: id пользователя;
            role_id: id роли;
        """
        self.user_id = user_id  # noqa: WPS601 переопределяем атрибуты класса
        self.role_id = role_id  # noqa: WPS601 (это здесь необходимо)
