from typing import Dict, List, Optional, Type

from motor.core import AgnosticDatabase
from pydantic import BaseModel

from src.db_models.mongo_base_model import MongoBaseModel


class WatchProgressDocument(BaseModel):
    user_id: str
    movie_id: str
    progress: float

    @classmethod
    def from_mongo(cls: Type['WatchProgressDocument'], doc: Dict) -> 'WatchProgressDocument':
        return cls(**doc)


class WatchProgressModel(MongoBaseModel[WatchProgressDocument]):
    def __init__(self, database: AgnosticDatabase):
        super().__init__(database, 'watch_progress', WatchProgressDocument.from_mongo)

    async def update_progress(self, watch_progress_document: WatchProgressDocument) -> None:
        query = {'user_id': watch_progress_document.user_id, 'movie_id': watch_progress_document.movie_id}
        update_data = {'$set': {'progress': watch_progress_document.progress}}
        await self.collection.update_one(query, update_data, upsert=True)

    async def get_progress(self, user_id: str, movie_id: str) -> Optional[WatchProgressDocument]:
        return await self.find_one({'user_id': user_id, 'movie_id': movie_id})

    async def get_all_progresses(self, user_id: str) -> List[WatchProgressDocument]:
        return await self.find({'user_id': user_id})
