"""Модель жанра."""
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from tests.functional import settings
from tests.functional.models.movies.base import Base


class Genre(Base):
    """Модель жанра кинопроизведения."""

    __tablename__ = 'genre_film_work'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(
        String(settings.long_char_field_len),
        unique=True,
        nullable=False,
    )
    description = Column(
        String(settings.long_char_field_len),  # TODO: подобрать более подходящий тип
        unique=True,
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        """Строковое представление записи жанра.

        Returns:
            строка, содержащая имя жанра.
        """
        return '<Genre {title}>'.format(title=self.title)


class GenreFilmwork(Base):
    """Модель, реализующая связь многие ко многим между жанрами и кинопроизведениями."""

    __tablename__ = 'users_roles'

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
    genre_id = Column(
        UUID,
        ForeignKey('roles.id', ondelete='CASCADE'),
        nullable=False,
    )
    genre_filmwork_idx = UniqueConstraint('film_work_id', 'genre_id')

    def __init__(self, film_work_id: UUID, genre_id: UUID) -> None:
        """Инициализация записи роли.

        Args:
            film_work_id: id кинопроизведения;
            genre_id: id жанра;
        """
        self.film_work_id = film_work_id  # noqa: WPS601 переопределяем атрибуты класса
        self.genre_id = genre_id  # noqa: WPS601 (это здесь необходимо)
