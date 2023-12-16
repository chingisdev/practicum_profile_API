"""Фикстура клиента Postgres."""
import asyncio

import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.schema import CreateSchema, DropSchema

from src.models.base import Base
from tests.functional.settings import test_settings

event.listen(Base.metadata, 'before_create', CreateSchema('content'))
event.listen(Base.metadata, 'after_drop', DropSchema('content', cascade=True))


class AsyncSimplePostgresClient:
    """Класс упрощённого асинхронного клиента базы данных Postgres."""

    def __init__(self, url: str):
        """Инициализация экземпляра упрощённого для тестов клиента базы данных Postgres.

        Args:
            url: - url для соединения с postgres;
        """
        pg_echo = test_settings.POSTGRES_ECHO == 'True'
        self.engine = create_async_engine(
            url,
            echo=pg_echo,
            future=True,
        )

        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def create_database(self) -> None:
        """Метод для создания базы данных Postgres."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def purge_database(self) -> None:
        """Метод для удаления базы данных Postgres."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope='function')  # Тесты не должны влиять друг на друга
async def pg_session():
    """Получить экземпляр ceccии клиента postgres.

    Yields:
        session:
    """
    postgres_client = AsyncSimplePostgresClient(
        url='postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}'.format(
            user=test_settings.POSTGRES_USER,
            password=test_settings.POSTGRES_PASSWORD,
            host=test_settings.POSTGRES_HOST,
            port=test_settings.POSTGRES_PORT,
            db_name=test_settings.POSTGRES_DB,
        ),
    )
    await postgres_client.create_database()
    async with postgres_client.async_session() as session:
        yield session
    await postgres_client.purge_database()  # Тесты не должны влиять друг на друга


if __name__ == '__main__':
    # Явное удаление схемы в бд, если она по какой-то причине не удалилась при закрытии клиента:
    postgres_client = AsyncSimplePostgresClient(
        url='postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}'.format(
            user=test_settings.POSTGRES_USER,
            password=test_settings.POSTGRES_PASSWORD,
            host=test_settings.POSTGRES_HOST,
            port=test_settings.POSTGRES_PORT,
            db_name=test_settings.POSTGRES_DB,
        ),
    )
    asyncio.run(postgres_client.purge_database())
