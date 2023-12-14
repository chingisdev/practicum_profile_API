"""Конфигурация pytest."""
pytest_plugins = (
    'tests.scheduler_api_tests.fixtures.api_client',
    'tests.scheduler_api_tests.fixtures.event_loop',
)
