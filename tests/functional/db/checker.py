"""Утилита для получения содержимого таблицы базы данных."""
from sqlalchemy.future import select

from src.models.base import Base


async def get_table_content(pg_session, model) -> list[Base]:
    """Утилита для получения содержимого таблицы базы данных.

    Args:
        pg_session: асинхронная сессия sqlalchemy;
        model: модель в которую нужно добавить запись;

    Returns:
        list[Base]: список записей таблицы.
    """
    response = await pg_session.execute(select(model))
    return response.scalars().all()
