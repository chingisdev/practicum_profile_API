"""Базовый класс моделей Postgres."""
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

Base = declarative_base(
    metadata=MetaData(
        schema='content',
    ),
)
