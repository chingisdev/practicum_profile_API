"""Модель кинопроизведения."""
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from src.core.config import settings
from src.models.base import Base


class Person(Base):
    """Модель персоны."""

    __tablename__ = 'person'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    full_name = Column(
        String(settings.long_char_field_len),
        unique=True,
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        """Строковое представление записи персоны.

        Returns:
            строка, содержащая полное имя персоны.
        """
        return '<Person {full_name}>'.format(full_name=self.full_name)


class PersonFilmwork(Base):
    """Модель, реализующая связь многие ко многим между персонами и кинопроизведениями."""

    __tablename__ = 'person_film_work'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    film_work_id = Column(
        UUID,
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    person_id = Column(
        UUID,
        ForeignKey('roles.id', ondelete='CASCADE'),
        nullable=False,
    )
    person_filmwork_idx = UniqueConstraint('film_work_id', 'person_id')

    def __init__(self, film_work_id: UUID, person_id: UUID) -> None:
        """Инициализация записи связи персоны и фильма.

        Args:
            film_work_id: id кинопроизведения;
            person_id: id персоны;
        """
        self.film_work_id = film_work_id  # noqa: WPS601 переопределяем атрибуты класса
        self.person_id = person_id  # noqa: WPS601 (это здесь необходимо)
