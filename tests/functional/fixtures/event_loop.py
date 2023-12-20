"""Фикстура цикла событий."""
import asyncio

import pytest


@pytest.fixture(scope='session')  # session: фикстура будет удалена в конце
# тест-сессии.
def event_loop():
    """
    Создать экземпляр исходного цикла событий для каждого теста.

    https://github.com/tiangolo/fastapi/issues/5692

    Yields:
        loop: цикл событий asyncio
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
