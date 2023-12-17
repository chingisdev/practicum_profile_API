"""Фикстура клиента Redis."""
import pytest_asyncio
from redis.asyncio import Redis

from tests.functional.settings import test_settings


@pytest_asyncio.fixture(scope='function')
async def movies_api_redis_client():
    """Получить экземпляр клиента redis для movies api.

    Yields:
        es_client: клиент redis
    """
    redis = await Redis.from_url(
        'redis://{host}:{port}'.format(
            host=test_settings.movies_redis_host,
            port=test_settings.movies_redis_port,
        ),
    )

    await redis.flushall()
    yield redis
    await redis.flushall()  # тесты не должны влиять друг на друга
    await redis.close()
