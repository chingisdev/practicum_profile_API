"""Конфигурация pytest."""
pytest_plugins = (
    'tests.functional.fixtures.api_client',
    'tests.functional.fixtures.event_loop',
    'tests.functional.fixtures.postgres_client',
    'tests.functional.fixtures.redis_client',
)
