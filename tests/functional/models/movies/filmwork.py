"""Модель кинопроизведения."""
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, String
from sqlalchemy.dialects.postgresql import UUID

from tests.functional import settings
from tests.functional.models.movies.base import Base


class Filmwork(Base):
    """Модель кинопроизведения."""

    __tablename__ = 'filmwork'

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
    description = Column(
        String(settings.long_char_field_len),  # TODO: подобрать более подходящий тип
        unique=True,
        nullable=False,
    )
    file_path = Column(
        String(settings.long_char_field_len),
        unique=True,
        nullable=False,
    )
    rating = Column(
        Float(),
        nullable=False,
    )
    type = Column(
        String(settings.long_char_field_len),
        unique=True,
        nullable=False,
    )
    creation_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        """Строковое представление записи кинопроизведения.

        Returns:
            строка, содержащая имя кинопроизведения.
        """
        return '<Filmwork {title}>'.format(title=self.title)
