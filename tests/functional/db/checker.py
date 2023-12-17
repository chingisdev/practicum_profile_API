"""Утилита для получения содержимого таблицы базы данных."""
from typing import Union

from sqlalchemy.future import select

from tests.functional.models.auth.base import Base as Auth_Base
from tests.functional.models.movies.base import Base as Movies_Base


async def get_table_content(pg_session, model) -> list[Union[Movies_Base, Auth_Base]]:
    """Утилита для получения содержимого таблицы базы данных.

    Args:
        pg_session: асинхронная сессия sqlalchemy;
        model: модель в которую нужно добавить запись;

    Returns:
        list[Base]: список записей таблицы.
    """
    response = await pg_session.execute(select(model))
    return response.scalars().all()
