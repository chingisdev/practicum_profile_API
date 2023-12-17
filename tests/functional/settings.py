"""Конфигурация тестов Profile API."""
from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    """Конфигурация тестов Profile API."""

    app_version: str = '0.0.1'
    app_version_details: str = (
        'разработка.'
    )
    project_name: str  # название проекта. используется в swagger-документации

    redis_host: str
    redis_port: int

    cache_life_time: int  # время жизни кэша redis

    # реквизиты бд profile и auth:

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_echo: str = 'True'

    # реквизиты бд movies

    movies_postgres_db: str
    movies_postgres_user: str
    movies_postgres_password: str
    movies_postgres_host: str
    movies_postgres_port: int
    movies_postgres_echo: str = 'True'

    standard_char_field_len: int = 64
    long_char_field_len: int = 128

    secret_key: str
    secret_key_refresh: str

    default_admin_password: str

    service_url: str


test_settings = TestSettings()  # type: ignore
