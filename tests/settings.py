"""Конфигурация тестов Profile API."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Конфигурация тестов Profile API."""

    service_url: str = 'http://localhost:8000'


test_settings = Settings()  # type: ignore
