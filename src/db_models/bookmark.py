from typing import Dict, List, Type

from motor.core import AgnosticDatabase
from pydantic import BaseModel

from src.db_models.mongo_base_model import MongoBaseModel


class BookmarkDocument(BaseModel):
    user_id: str
    movie_id: str

    @classmethod
    def from_mongo(cls: Type['BookmarkDocument'], doc: Dict) -> 'BookmarkDocument':
        return cls(**doc)


class BookmarkModel(MongoBaseModel[BookmarkDocument]):
    def __init__(self, database: AgnosticDatabase):
        super().__init__(database, 'bookmarks', BookmarkDocument.from_mongo)

    async def add_bookmark(self, user_id: str, movie_id: str) -> None:
        await self.collection.insert_one({'user_id': user_id, 'movie_id': movie_id})

    async def remove_bookmark(self, user_id: str, movie_id: str) -> None:
        await self.collection.delete_one({'user_id': user_id, 'movie_id': movie_id})

    async def get_user_bookmarks(self, user_id: str) -> List[BookmarkDocument]:
        return await self.find({'user_id': user_id})
