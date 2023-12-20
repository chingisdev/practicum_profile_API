"""Модель роли."""
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from tests.functional import settings
from tests.functional.models.auth.base import Base


class Role(Base):
    """Модель пользовательской роли."""

    __tablename__ = 'roles'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    title = Column(
        String(settings.long_char_field_len),
        unique=True,
        nullable=False,
    )
    permissions = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, title: str, permissions: int) -> None:
        """Инициализация записи роли.

        Args:
            title: имя роли;
            permissions: предоставляемые ролью права.
        """
        self.title = title  # noqa: WPS601 переопределяем атрибуты класса (это здесь необходимо)
        self.permissions = permissions  # noqa: WPS601

    def __repr__(self) -> str:
        """Строковое представление записи роли.

        Returns:
            строка, содержащая имя роли.
        """
        return '<Role {title}>'.format(title=self.title)
