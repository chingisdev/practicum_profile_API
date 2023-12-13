from enum import Enum
from typing import Dict, Type

from motor.core import AgnosticDatabase
from pydantic import BaseModel

from src.db_models.mongo_base_model import MongoBaseModel


class TargetType(Enum):
    movie = 'movie'
    review = 'review'


class LikeDocument(BaseModel):
    user_id: str
    target_id: str
    target_type: TargetType

    @classmethod
    def from_mongo(cls: Type['LikeDocument'], doc: Dict) -> 'LikeDocument':
        return cls(**doc)


class LikeModel(MongoBaseModel[LikeDocument]):
    def __init__(self, database: AgnosticDatabase):
        super().__init__(database, 'likes', LikeDocument.from_mongo)

    async def add_like(self, like_document: LikeDocument) -> None:
        await self.collection.insert_one(like_document.model_dump())

    async def remove_like(self, like_document: LikeDocument) -> None:
        await self.collection.delete_one(like_document.model_dump())
