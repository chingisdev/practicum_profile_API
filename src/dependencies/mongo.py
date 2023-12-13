from typing import TypeAlias

from motor.core import AgnosticClient

AsyncMongoClient: TypeAlias = AgnosticClient

mongo_client: AsyncMongoClient | None = None


def get_mongo_client() -> AsyncMongoClient | None:
    return mongo_client
