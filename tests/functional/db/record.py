"""Утилита для добавления записей в таблицу базы данных."""
from typing import Any, Union

from tests.functional.models.auth.base import Base as Auth_Base
from tests.functional.models.movies.base import Base as Movies_Base


async def add_record(
    pg_session,
    model,
    filler: dict[str, Any],
) -> list[Union[Movies_Base, Auth_Base]]:
    """Добавить запись в таблицу.

    Args:
        pg_session: асинхронная сессия sqlalchemy;
        model: модель в которую нужно добавить запись;
        filler: данные, для создания записи.

    Returns:
        Base: созданная запись.
    """
    new_record = model(**filler)
    pg_session.add(new_record)
    await pg_session.commit()
    await pg_session.refresh(new_record)
    return new_record
