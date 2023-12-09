from typing import Callable, Dict, Generic, List, TypeVar

from dependencies.mongo import AsyncMongoClient

PydanticEntity = TypeVar('PydanticEntity')


class MongoBaseModel(Generic[PydanticEntity]):
    def __init__(self, db_client: AsyncMongoClient, collection_name: str, factory: Callable[[Dict], PydanticEntity]):
        self.collection = db_client[collection_name]
        self.factory = factory

    async def find_one(self, query: dict) -> PydanticEntity:
        document = await self.collection.find_one(query)
        return self.factory(document)

    async def find(self, query: dict, skip: int = 0, limit: int = 0) -> List[PydanticEntity]:
        cursor = self.collection.find(query).skip(skip).limit(limit)
        documents = await cursor.to_list(length=limit)
        return [self.factory(doc) for doc in documents]
