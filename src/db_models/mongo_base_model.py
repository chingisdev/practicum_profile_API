from typing import Any, Callable, Generic, List, Optional, TypeVar

from motor.core import AgnosticDatabase

PydanticEntity = TypeVar('PydanticEntity')


class MongoBaseModel(Generic[PydanticEntity]):
    def __init__(self, database: AgnosticDatabase, collection_name: str, factory: Callable[[Any], PydanticEntity]):
        self.collection = database[collection_name]
        self.factory = factory

    async def find_one(self, query: dict) -> Optional[PydanticEntity]:
        document = await self.collection.find_one(query)
        if document is None:
            return None
        return self.factory(document)

    async def find(self, query: dict, skip: int = 0, limit: int = 0) -> List[PydanticEntity]:
        cursor = self.collection.find(query).skip(skip).limit(limit)
        documents = await cursor.to_list(length=limit)
        return [self.factory(doc) for doc in documents]
